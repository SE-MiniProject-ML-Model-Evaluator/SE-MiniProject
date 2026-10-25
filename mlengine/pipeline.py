"""C5 Data Pipeline: missing values (FR-07), encoding, and train/test split (FR-08)."""
import pandas as pd
from sklearn.model_selection import train_test_split

from datasets.services import load_dataframe


class DataPreparationError(Exception):
    """Raised with a user-readable message; the job is marked failed (Design Spec 5.4)."""


def handle_missing(df: pd.DataFrame, features, strategy: str) -> pd.DataFrame:
    df = df.copy()
    if strategy == "drop":
        return df.dropna(subset=features)
    if strategy == "mean_mode":
        for col in features:
            if df[col].isna().all():
                raise DataPreparationError(f"Column '{col}' has no values; remove it from the features.")
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(df[col].mode().iloc[0])
        return df
    missing = [c for c in features if df[c].isna().any()]
    if missing:
        raise DataPreparationError(
            f"Feature column(s) {', '.join(repr(c) for c in missing)} have missing values. "
            "Choose 'Drop rows' or 'Mean / mode imputation' in the configuration.")
    return df


def prepare(dataset):
    """Return X_train, X_test, y_train, y_test, task_type, class_labels for a configured dataset."""
    config = getattr(dataset, "config", None)
    if config is None:
        raise DataPreparationError("The dataset is not configured yet.")
    features, target = list(config.feature_columns), config.target_column
    df = load_dataframe(dataset)
    absent = [c for c in features + [target] if c not in df.columns]
    if absent:
        raise DataPreparationError(f"Column(s) not found in the file: {', '.join(absent)}.")

    df = df[features + [target]].dropna(subset=[target])          # rows without a target cannot be used
    df = handle_missing(df, features, config.missing_strategy)
    if len(df) < 10:
        raise DataPreparationError("Fewer than 10 usable rows remain after handling missing values.")

    X = pd.get_dummies(df[features], drop_first=False, dtype=float)   # one-hot encode categorical features
    y = df[target]
    task = config.task_type
    labels = None
    stratify = None
    if task == "classification":
        y = y.astype(str)
        labels = sorted(y.unique().tolist())
        if len(labels) < 2:
            raise DataPreparationError("The target column needs at least 2 different classes.")
        counts = y.value_counts()
        n_test = max(1, round(len(y) * config.test_size))
        if counts.min() >= 2 and n_test >= len(labels):
            stratify = y
    elif not pd.api.types.is_numeric_dtype(y):
        raise DataPreparationError(f"Regression needs a numeric target; '{target}' is not numeric.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.test_size, random_state=config.random_seed, stratify=stratify)
    return X_train, X_test, y_train, y_test, task, labels
