"""US-08 (FR-06): TC-06 target/feature selection."""
import pytest

from datasets.models import Dataset
from datasets.services import infer_task_type
from .conftest import csv_file, sample_bytes

pytestmark = pytest.mark.django_db

FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


@pytest.fixture
def iris(auth_client, user):
    auth_client.post("/datasets/upload/", {"file": csv_file("iris.csv", sample_bytes("iris.csv"))})
    return Dataset.objects.get(owner=user)


def test_configure_target_and_features(auth_client, iris):
    r = auth_client.post(f"/datasets/{iris.id}/configure/", {"target": "species", "features": FEATURES})
    assert r.status_code == 302
    iris.refresh_from_db()
    assert iris.config.target_column == "species"
    assert iris.config.feature_columns == FEATURES
    assert iris.config.task_type == "classification"


def test_target_cannot_be_a_feature(auth_client, iris):
    r = auth_client.post(f"/datasets/{iris.id}/configure/", {"target": "species", "features": ["species"]})
    assert r.status_code == 200 and b"cannot also be a feature" in r.content


def test_at_least_one_feature_required(auth_client, iris):
    r = auth_client.post(f"/datasets/{iris.id}/configure/", {"target": "species"})
    assert r.status_code == 200 and not hasattr(Dataset.objects.get(pk=iris.pk), "config")


def test_api_put_config(auth_client, iris):
    r = auth_client.put(f"/api/datasets/{iris.id}/config", {"target": "species", "features": FEATURES},
                        content_type="application/json")
    assert r.status_code == 200 and r.json()["saved"] is True
    r = auth_client.put(f"/api/datasets/{iris.id}/config", {"target": "nope", "features": FEATURES},
                        content_type="application/json")
    assert r.status_code == 400 and r.json()["error"]["code"] == "VALIDATION_ERROR"


def test_regression_target_detected(auth_client, user):
    auth_client.post("/datasets/upload/", {"file": csv_file("diabetes.csv", sample_bytes("diabetes.csv"))})
    ds = Dataset.objects.get(owner=user)
    auth_client.post(f"/datasets/{ds.id}/configure/", {"target": "disease_progression", "features": ["age", "bmi"]})
    ds.refresh_from_db()
    assert ds.config.task_type == "regression"


def test_infer_task_type():
    import pandas as pd
    assert infer_task_type(pd.Series(["a", "b"])) == "classification"
    assert infer_task_type(pd.Series([0, 1, 1, 0])) == "classification"
    assert infer_task_type(pd.Series([x * 1.5 for x in range(100)])) == "regression"
