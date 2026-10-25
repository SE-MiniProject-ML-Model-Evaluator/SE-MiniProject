"""Saving a dataset configuration (FR-06 to FR-08), shared by the page and the API."""
from .models import DatasetConfig
from .services import infer_task_type, load_dataframe


def save_config(dataset, cleaned):
    df = load_dataframe(dataset)
    task_type = infer_task_type(df[cleaned["target"]])
    defaults = {
        "target_column": cleaned["target"],
        "feature_columns": list(cleaned["features"]),
        "task_type": task_type,
    }
    for field in ("missing_strategy", "random_seed"):
        if cleaned.get(field) not in (None, ""):
            defaults[field] = cleaned[field]
    if cleaned.get("test_size") not in (None, ""):
        defaults["test_size"] = round(float(cleaned["test_size"]) / 100.0, 4)   # form uses percent
    config, _ = DatasetConfig.objects.update_or_create(dataset=dataset, defaults=defaults)
    return config


def initial_from(dataset):
    config = getattr(dataset, "config", None)
    if not config:
        return {}
    return {"target": config.target_column, "features": config.feature_columns,
            "missing_strategy": config.missing_strategy, "test_size": round(config.test_size * 100),
            "random_seed": config.random_seed}
