"""US-11 (FR-09) and US-12 (FR-11, NFR-06): TC-07, TC-08, TC-16, TC-18."""
import pytest

from mlengine.catalogue import CATALOGUE, InvalidModelConfig, models_for, resolve_params
from mlengine.models import Evaluation

pytestmark = pytest.mark.django_db


def test_catalogue_contains_required_models():
    assert set(models_for("classification")) == {"logistic_regression", "decision_tree", "random_forest", "knn", "svm"}
    assert set(models_for("regression")) == {"linear_regression", "decision_tree_regressor",
                                             "random_forest_regressor"}
    assert all(len(spec["params"]) >= 1 for spec in CATALOGUE.values())


def test_resolve_params_defaults_and_validation():
    assert resolve_params("random_forest") == {"n_estimators": 100, "max_depth": None}
    tuned = resolve_params("random_forest", {"n_estimators": "50", "max_depth": 5})
    assert tuned == {"n_estimators": 50, "max_depth": 5}
    with pytest.raises(InvalidModelConfig):
        resolve_params("random_forest", {"n_estimators": 0})
    with pytest.raises(InvalidModelConfig):
        resolve_params("random_forest", {"bogus": 1})


def test_api_models_lists_catalogue(auth_client):
    r = auth_client.get("/api/models")
    assert r.status_code == 200 and len(r.json()) == 8


def test_train_page_only_offers_matching_models(auth_client, iris, diabetes):
    page = auth_client.get(f"/evaluations/new/{iris.id}/").content
    assert b"Random Forest" in page and b"Linear Regression" not in page
    page = auth_client.get(f"/evaluations/new/{diabetes.id}/").content
    assert b"Linear Regression" in page and b"Logistic Regression" not in page


def test_train_two_models_completes(auth_client, iris):  # TC-07 (status flow)
    r = auth_client.post(f"/evaluations/new/{iris.id}/", {"models": ["logistic_regression", "random_forest"]})
    assert r.status_code == 302 and r["Location"].startswith("/evaluations/run/")
    evaluations = Evaluation.objects.filter(dataset=iris)
    assert evaluations.count() == 2
    assert all(e.status == "completed" for e in evaluations)
    assert all(e.test_rows == 38 for e in evaluations)
    page = auth_client.get(r["Location"])
    assert page.status_code == 200 and b"Logistic Regression" in page.content


def test_train_requires_a_model(auth_client, iris):
    r = auth_client.post(f"/evaluations/new/{iris.id}/", {})
    assert r.status_code == 200 and b"Select at least one model" in r.content


def test_api_create_and_get_evaluation(auth_client, iris):
    r = auth_client.post("/api/evaluations", {"dataset_id": iris.id, "model": "random_forest",
                                              "hyperparameters": {"n_estimators": 50, "max_depth": 5}},
                         content_type="application/json")
    assert r.status_code == 202
    body = auth_client.get(f"/api/evaluations/{r.json()['evaluation_id']}").json()
    assert body["status"] == "completed" and body["hyperparameters"] == {"n_estimators": 50, "max_depth": 5}


def test_api_rejects_wrong_model(auth_client, iris):
    r = auth_client.post("/api/evaluations", {"dataset_id": iris.id, "model": "linear_regression"},
                         content_type="application/json")
    assert r.status_code == 422 and r.json()["error"]["code"] == "INVALID_MODEL_CONFIG"


def test_failed_job_is_contained_and_next_job_runs(auth_client, user):  # TC-16 / NFR-06
    from datasets.config import save_config
    from .conftest import load
    ds = load(user, "iris_missing.csv")
    save_config(ds, {"target": "species", "features": ["sepal_length", "petal_width"], "missing_strategy": "none",
                     "test_size": 20, "random_seed": 1})
    auth_client.post(f"/evaluations/new/{ds.id}/", {"models": ["logistic_regression"]})
    failed = Evaluation.objects.get(dataset=ds)
    assert failed.status == "failed" and "missing values" in failed.error_message
    save_config(ds, {"target": "species", "features": ["sepal_length", "petal_width"],
                     "missing_strategy": "mean_mode", "test_size": 20, "random_seed": 1})
    auth_client.post(f"/evaluations/new/{ds.id}/", {"models": ["logistic_regression"]})
    assert Evaluation.objects.filter(dataset=ds, status="completed").count() == 1


def test_unconfigured_dataset_redirects_to_configure(auth_client, user):
    from .conftest import load
    ds = load(user, "iris.csv")
    r = auth_client.get(f"/evaluations/new/{ds.id}/")
    assert r.status_code == 302 and r["Location"] == f"/datasets/{ds.id}/configure/"


def test_other_users_cannot_see_evaluations(auth_client, iris, other_user, client):  # TC-18
    auth_client.post(f"/evaluations/new/{iris.id}/", {"models": ["knn"]})
    evaluation = Evaluation.objects.get()
    client.force_login(other_user)
    assert client.get(f"/evaluations/{evaluation.id}/").status_code == 404
    assert client.get(f"/api/evaluations/{evaluation.id}").status_code == 404
    assert client.get(f"/evaluations/run/{evaluation.batch}/").status_code == 404
    assert client.get(f"/evaluations/new/{iris.id}/").status_code == 404
    assert client.get("/api/evaluations").json() == []


def test_regression_models_train(auth_client, diabetes):  # TC-08 (training part)
    auth_client.post(f"/evaluations/new/{diabetes.id}/",
                     {"models": ["linear_regression", "decision_tree_regressor", "random_forest_regressor"]})
    assert Evaluation.objects.filter(dataset=diabetes, status="completed").count() == 3
