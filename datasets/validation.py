"""FR-04 / SR-03: upload validation. Files are parsed as data only, never executed or unpickled."""
import io

import pandas as pd
from django.conf import settings

ALLOWED_CONTENT_TYPES = {
    "text/csv", "application/csv", "text/plain", "application/vnd.ms-excel",
    "text/comma-separated-values", "application/octet-stream", "",
}
BINARY_SIGNATURES = (b"MZ", b"PK\x03\x04", b"\x7fELF", b"%PDF", b"\x89PNG", b"\xd0\xcf\x11\xe0")
MIN_ROWS, MIN_COLS = 20, 2


class UploadError(Exception):
    def __init__(self, code, message, http_status=400, details=None):
        super().__init__(message)
        self.code, self.message, self.http_status, self.details = code, message, http_status, details or {}


def column_type(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series):
        return "categorical"
    return "numeric" if pd.api.types.is_numeric_dtype(series) else "categorical"


def _looks_numeric(text: str) -> bool:
    try:
        float(str(text))
        return True
    except ValueError:
        return False


def validate_upload(uploaded_file):
    """Validate an uploaded CSV and return (raw_bytes, dataframe, columns).

    Raises UploadError with a specific code/message for every rejection reason.
    """
    name = uploaded_file.name or ""
    if not name.lower().endswith(".csv"):
        raise UploadError("UNSUPPORTED_FILE", "Only .csv files are accepted.", 415)

    max_bytes = settings.MLME_MAX_UPLOAD_BYTES
    if uploaded_file.size > max_bytes:
        raise UploadError("FILE_TOO_LARGE", "The uploaded file exceeds the 50 MB limit.", 413,
                          {"max_size_mb": max_bytes // (1024 * 1024)})

    content_type = (getattr(uploaded_file, "content_type", "") or "").split(";")[0].strip().lower()
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise UploadError("UNSUPPORTED_FILE", "The file type is not CSV.", 415, {"content_type": content_type})

    raw = uploaded_file.read()
    head = raw[:8192]
    if head.startswith(BINARY_SIGNATURES) or b"\x00" in head:
        raise UploadError("UNSUPPORTED_FILE", "The file is not a text CSV file.", 415)
    if not raw.strip():
        raise UploadError("VALIDATION_ERROR", "The file is empty.")

    df = None
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            df = pd.read_csv(io.BytesIO(raw), encoding=encoding, skipinitialspace=True)
            break
        except UnicodeDecodeError:
            continue
        except (pd.errors.ParserError, pd.errors.EmptyDataError, ValueError) as exc:
            raise UploadError("UNSUPPORTED_FILE", f"The file could not be read as CSV: {exc}".split("\n")[0], 415)
    if df is None:
        raise UploadError("UNSUPPORTED_FILE", "The file encoding is not supported (use UTF-8).", 415)

    headers = [str(c) for c in df.columns]
    if any(h.startswith("Unnamed:") for h in headers) or all(_looks_numeric(h) for h in headers):
        raise UploadError("VALIDATION_ERROR", "The first row must be a header row with column names.")
    if df.shape[1] < MIN_COLS:
        raise UploadError("VALIDATION_ERROR", f"The dataset needs at least {MIN_COLS} columns.",
                          details={"columns": int(df.shape[1])})
    if df.shape[0] < MIN_ROWS:
        raise UploadError("VALIDATION_ERROR", f"The dataset needs at least {MIN_ROWS} data rows.",
                          details={"rows": int(df.shape[0])})

    df.columns = headers
    columns = [{"name": c, "type": column_type(df[c])} for c in headers]
    return raw, df, columns
