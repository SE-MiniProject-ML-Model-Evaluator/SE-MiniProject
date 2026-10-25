"""C8 Job Manager: runs training/evaluation in background threads (FR-11, NFR-06)."""
import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.db import close_old_connections
from django.utils import timezone

from . import metrics
from .catalogue import CATALOGUE, build_model, resolve_params
from .models import Evaluation
from .pipeline import DataPreparationError, prepare

logger = logging.getLogger(__name__)
_executor = None
SOFT_LIMIT_S = 60   # NFR-02 target


def _get_executor():
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=settings.MLME_JOB_WORKERS, thread_name_prefix="mlme-job")
    return _executor


def start_evaluations(owner, dataset, model_keys, hyperparameters=None):
    """Create one queued Evaluation per model (same batch) and hand them to the worker pool."""
    hyperparameters = hyperparameters or {}
    batch = uuid.uuid4().hex[:12]
    created = []
    for key in model_keys:
        params = resolve_params(key, hyperparameters.get(key))
        created.append(Evaluation.objects.create(
            owner=owner, dataset=dataset, batch=batch, model_key=key, model_label=CATALOGUE[key]["label"],
            hyperparameters=params, task_type=dataset.config.task_type))
    for evaluation in created:
        submit(evaluation.id)
    return batch, created


def submit(evaluation_id):
    if settings.MLME_SYNC_JOBS:
        run_evaluation(evaluation_id)
    else:
        _get_executor().submit(_run_in_thread, evaluation_id)


def _run_in_thread(evaluation_id):
    close_old_connections()
    try:
        run_evaluation(evaluation_id)
    finally:
        close_old_connections()


def run_evaluation(evaluation_id):
    """Train and evaluate one model. Any error marks only this evaluation as failed."""
    evaluation = Evaluation.objects.select_related("dataset__config").get(pk=evaluation_id)
    evaluation.status = "running"
    evaluation.save(update_fields=["status"])
    started = time.monotonic()
    try:
        X_train, X_test, y_train, y_test, task, labels = prepare(evaluation.dataset)
        model = build_model(evaluation.model_key, evaluation.hyperparameters,
                            evaluation.dataset.config.random_seed)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        evaluation.metrics = metrics.compute(task, y_test, y_pred, labels)
        evaluation.train_rows, evaluation.test_rows = len(X_train), len(X_test)
        evaluation.status = "completed"
    except DataPreparationError as exc:
        evaluation.status, evaluation.error_message = "failed", str(exc)
    except Exception as exc:  # NFR-06: contain any failure to this job
        logger.exception("Evaluation %s failed", evaluation_id)
        evaluation.status = "failed"
        evaluation.error_message = f"Training failed: {type(exc).__name__}: {str(exc)[:300]}"
    evaluation.duration_s = round(time.monotonic() - started, 3)
    if evaluation.duration_s > SOFT_LIMIT_S:
        logger.warning("Evaluation %s took %.1fs (target %ss)", evaluation_id, evaluation.duration_s, SOFT_LIMIT_S)
    evaluation.finished_at = timezone.now()
    evaluation.save()
    return evaluation
