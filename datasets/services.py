"""C4 Dataset Service / C12 File Storage helpers."""
import io
import math
import uuid
from pathlib import Path

import pandas as pd
from django.conf import settings

from .models import Dataset
from .validation import validate_upload

PREVIEW_ROWS = 20


def store_dataset(owner, uploaded_file) -> Dataset:
    """Validate, save under a random name outside the web root, and record metadata (FR-03, FR-04)."""
    raw, df, columns = validate_upload(uploaded_file)
    folder = Path(settings.MEDIA_ROOT) / "datasets"
    folder.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}.csv"
    (folder / stored_name).write_bytes(raw)
    return Dataset.objects.create(
        owner=owner, original_name=Path(uploaded_file.name).name[:255], stored_name=stored_name,
        size_bytes=len(raw), n_rows=int(df.shape[0]), n_cols=int(df.shape[1]), columns=columns,
    )


def load_dataframe(dataset: Dataset) -> pd.DataFrame:
    raw = dataset.path.read_bytes()
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            df = pd.read_csv(io.BytesIO(raw), encoding=encoding, skipinitialspace=True)
            df.columns = [str(c) for c in df.columns]
            return df
        except UnicodeDecodeError:
            continue
    raise ValueError("Unsupported encoding")


def _clean(value):
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def preview(dataset: Dataset, n=PREVIEW_ROWS):
    """FR-05: first n rows as a list of dicts (missing values -> None)."""
    df = load_dataframe(dataset).head(n)
    return [{col: _clean(val) for col, val in row.items()} for row in df.to_dict(orient="records")]


def infer_task_type(series: pd.Series) -> str:
    """Classification for text/boolean targets or numeric targets with few distinct values; else regression."""
    s = series.dropna()
    if not pd.api.types.is_numeric_dtype(s) or pd.api.types.is_bool_dtype(s):
        return "classification"
    is_integer_like = bool((s % 1 == 0).all()) if len(s) else True
    if is_integer_like and s.nunique() <= 15:
        return "classification"
    return "regression"
