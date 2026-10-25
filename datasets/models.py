"""C4 Dataset Service data model (Design Spec 2.6: DATASET, DATASET_CONFIG)."""
from pathlib import Path

from django.conf import settings
from django.db import models


class Dataset(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="datasets")
    original_name = models.CharField(max_length=255)
    stored_name = models.CharField(max_length=64, unique=True)   # random name, never the user's filename
    size_bytes = models.PositiveBigIntegerField()
    n_rows = models.PositiveIntegerField()
    n_cols = models.PositiveIntegerField()
    columns = models.JSONField(default=list)                     # [{"name": ..., "type": "numeric"|"categorical"}]
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.original_name} ({self.owner})"

    @property
    def path(self) -> Path:
        return Path(settings.MEDIA_ROOT) / "datasets" / self.stored_name

    @property
    def column_names(self):
        return [c["name"] for c in self.columns]

    @property
    def is_configured(self):
        config = getattr(self, "config", None)
        return bool(config and config.target_column and config.feature_columns)


class DatasetConfig(models.Model):
    MISSING_CHOICES = [
        ("none", "None (keep as is)"),
        ("drop", "Drop rows with missing values"),
        ("mean_mode", "Mean / mode imputation"),
    ]
    TASK_CHOICES = [("classification", "Classification"), ("regression", "Regression")]

    dataset = models.OneToOneField(Dataset, on_delete=models.CASCADE, related_name="config")
    target_column = models.CharField(max_length=255)
    feature_columns = models.JSONField(default=list)
    missing_strategy = models.CharField(max_length=16, choices=MISSING_CHOICES, default="none")
    test_size = models.FloatField(default=0.2)          # fraction, 0.10 - 0.50 (FR-08)
    random_seed = models.IntegerField(default=42)
    task_type = models.CharField(max_length=16, choices=TASK_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Config for {self.dataset_id}: target={self.target_column}"
