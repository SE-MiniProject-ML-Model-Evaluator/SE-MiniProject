from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from accounts.permissions import get_owned_or_404
from audit.services import log_event
from datasets.models import Dataset
from .catalogue import InvalidModelConfig
from .forms import TrainForm
from .jobs import start_evaluations
from .models import Evaluation


@login_required
def evaluation_list(request):
    """FR-16: history of the user's evaluations (newest first)."""
    evaluations = Evaluation.objects.filter(owner=request.user).select_related("dataset")[:500]
    return render(request, "mlengine/list.html", {"evaluations": evaluations})


@login_required
def train(request, dataset_id):
    dataset = get_owned_or_404(Dataset.objects.select_related("config"), request.user, dataset_id)
    if not dataset.is_configured:
        messages.error(request, "Configure the target and feature columns first.")
        return redirect(f"/datasets/{dataset.id}/configure/")
    form = TrainForm(request.POST if request.method == "POST" else None, task_type=dataset.config.task_type)
    if request.method == "POST" and form.is_valid():
        try:
            batch, _ = start_evaluations(request.user, dataset, form.cleaned_data["models"],
                                         form.hyperparameters())
        except InvalidModelConfig as exc:
            form.add_error(None, str(exc))
        else:
            return redirect(f"/evaluations/run/{batch}/")
    return render(request, "mlengine/train.html", {"dataset": dataset, "config": dataset.config, "form": form})


@login_required
def run_results(request, batch):
    evaluations = list(Evaluation.objects.filter(owner=request.user, batch=batch)
                       .select_related("dataset").order_by("id"))
    if not evaluations:
        raise Http404("Not found")
    return render(request, "mlengine/results.html", {
        "evaluations": evaluations, "dataset": evaluations[0].dataset, "batch": batch,
        "pending": [e.id for e in evaluations if not e.is_done]})


@login_required
def evaluation_detail(request, pk):
    evaluation = get_owned_or_404(Evaluation.objects.select_related("dataset"), request.user, pk)
    return render(request, "mlengine/results.html", {
        "evaluations": [evaluation], "dataset": evaluation.dataset, "batch": evaluation.batch,
        "pending": [] if evaluation.is_done else [evaluation.id]})


@login_required
@require_POST
def evaluation_delete(request, pk):
    """FR-16: delete one evaluation from the history."""
    evaluation = get_owned_or_404(Evaluation.objects.all(), request.user, pk)
    label = f"{evaluation.model_label} on {evaluation.dataset.original_name}"
    evaluation.delete()
    log_event("evaluation_delete", user=request.user, request=request, detail=label)
    messages.success(request, f"Deleted evaluation: {label}.")
    return redirect("/evaluations/")
