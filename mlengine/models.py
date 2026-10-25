"""EVALUATION entity (Design Spec 2.6)."""
from django.conf import settings
from django.db import models


class Evaluation(models.Model):
    STATUS_CHOICES = [("queued", "Queued"), ("running", "Running"), ("completed", "Completed"), ("failed", "Failed")]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluations")
    dataset = models.ForeignKey("datasets.Dataset", on_delete=models.CASCADE, related_name="evaluations")
    batch = models.CharField(max_length=32, db_index=True)       # models started together share a batch
    model_key = models.CharField(max_length=64)
    model_label = models.CharField(max_length=100)
    hyperparameters = models.JSONField(default=dict)
    task_type = models.CharField(max_length=16)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="queued")
    metrics = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    train_rows = models.PositiveIntegerField(null=True, blank=True)
    test_rows = models.PositiveIntegerField(null=True, blank=True)
    duration_s = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "id"]

    def __str__(self):
        return f"{self.model_label} on {self.dataset_id} [{self.status}]"

    @property
    def is_done(self):
        return self.status in ("completed", "failed")

    def as_api(self):
        return {"id": self.id, "status": self.status, "task_type": self.task_type, "model": self.model_key,
                "model_label": self.model_label, "dataset_id": self.dataset_id,
                "hyperparameters": self.hyperparameters,
                "metrics": self.metrics if self.status == "completed" else None,
                "error_message": self.error_message or None, "duration_s": self.duration_s,
                "created_at": self.created_at.isoformat()}
