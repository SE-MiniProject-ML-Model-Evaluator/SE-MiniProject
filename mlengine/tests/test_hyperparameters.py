"""US-15 (FR-10): TC-07 step 2 - edit at least two hyperparameters per model."""
import pytest

from mlengine.models import Evaluation

pytestmark = pytest.mark.django_db


def test_train_page_shows_hyperparameters_with_defaults(auth_client, iris):
    page = auth_client.get(f"/evaluations/new/{iris.id}/").content.decode()
    assert 'name="hp__random_forest__n_estimators"' in page and 'value="100"' in page
    assert 'name="hp__random_forest__max_depth"' in page
    assert 'name="hp__knn__n_neighbors"' in page


def test_custom_hyperparameters_are_used(auth_client, iris):  # TC-07 step 2
    r = auth_client.post(f"/evaluations/new/{iris.id}/", {
        "models": ["random_forest", "logistic_regression"],
        "hp__random_forest__n_estimators": "50", "hp__random_forest__max_depth": "5",
        "hp__logistic_regression__C": "0.5"})
    assert r.status_code == 302
    rf = Evaluation.objects.get(model_key="random_forest")
    assert rf.hyperparameters == {"n_estimators": 50, "max_depth": 5} and rf.status == "completed"
    lr = Evaluation.objects.get(model_key="logistic_regression")
    assert lr.hyperparameters["C"] == 0.5 and lr.hyperparameters["max_iter"] == 1000
    page = auth_client.get(r["Location"]).content
    assert b"n_estimators=50" in page and b"max_depth=5" in page


def test_blank_values_use_defaults_or_none(auth_client, iris):
    auth_client.post(f"/evaluations/new/{iris.id}/", {
        "models": ["decision_tree"], "hp__decision_tree__max_depth": "", "hp__decision_tree__criterion": "entropy"})
    e = Evaluation.objects.get()
    assert e.hyperparameters == {"max_depth": None, "min_samples_split": 2, "criterion": "entropy"}


def test_out_of_range_value_rejected(auth_client, iris):
    r = auth_client.post(f"/evaluations/new/{iris.id}/", {
        "models": ["random_forest"], "hp__random_forest__n_estimators": "0"})
    assert r.status_code == 200 and Evaluation.objects.count() == 0


def test_regression_choice_param(auth_client, diabetes):
    auth_client.post(f"/evaluations/new/{diabetes.id}/", {
        "models": ["linear_regression"], "hp__linear_regression__fit_intercept": "False"})
    assert Evaluation.objects.get().hyperparameters == {"fit_intercept": False}
