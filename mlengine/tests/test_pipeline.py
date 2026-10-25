"""US-09 (FR-07) and US-10 (FR-08): TC-06."""
import numpy as np
import pandas as pd
import pytest

from datasets.config import save_config
from mlengine.pipeline import DataPreparationError, handle_missing, prepare
from .conftest import load

pytestmark = pytest.mark.django_db
FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def configure(ds, **kw):
    cfg = {"target": "species", "features": FEATURES, "missing_strategy": "none", "test_size": 25,
           "random_seed": 42, **kw}
    save_config(ds, cfg)
    ds.refresh_from_db()
    return ds


def test_split_sizes_and_reproducibility(iris):
    X_train, X_test, y_train, y_test, task, labels = prepare(iris)
    assert (len(X_train), len(X_test)) == (112, 38)       # 75 / 25 split of 150 rows
    assert task == "classification" and labels == ["setosa", "versicolor", "virginica"]
    again = prepare(iris)
    assert list(again[1].index) == list(X_test.index)      # same seed -> same split


def test_different_seed_changes_split(iris):
    first = list(prepare(iris)[1].index)
    configure(iris, random_seed=7)
    assert list(prepare(iris)[1].index) != first


@pytest.mark.parametrize("size", [5, 60])
def test_test_size_out_of_range_rejected(auth_client, iris, size):
    r = auth_client.post(f"/datasets/{iris.id}/configure/",
                         {"target": "species", "features": FEATURES, "test_size": size})
    assert r.status_code == 200 and b"between 10% and 50%" in r.content


def test_missing_values_strategies(user):
    ds = load(user, "iris_missing.csv")
    configure(ds, missing_strategy="none")
    with pytest.raises(DataPreparationError, match="missing values"):
        prepare(ds)
    configure(ds, missing_strategy="drop")
    X_train, X_test, *_ = prepare(ds)
    assert len(X_train) + len(X_test) < 150 and not X_train.isna().any().any()
    configure(ds, missing_strategy="mean_mode")
    X_train, X_test, *_ = prepare(ds)
    assert len(X_train) + len(X_test) == 150 and not X_train.isna().any().any()


def test_mean_mode_imputation_values():
    df = pd.DataFrame({"n": [1.0, np.nan, 3.0], "c": ["x", None, "x"]})
    out = handle_missing(df, ["n", "c"], "mean_mode")
    assert out.loc[1, "n"] == 2.0 and out.loc[1, "c"] == "x"


def test_categorical_features_are_one_hot_encoded(user):
    ds = load(user, "iris.csv")
    save_config(ds, {"target": "sepal_length", "features": ["species", "petal_length"], "missing_strategy": "none",
                     "test_size": 20, "random_seed": 1})
    ds.refresh_from_db()
    X_train, *_, task, _ = prepare(ds)
    assert task == "regression"
    assert {"species_setosa", "species_versicolor", "species_virginica"} <= set(X_train.columns)
