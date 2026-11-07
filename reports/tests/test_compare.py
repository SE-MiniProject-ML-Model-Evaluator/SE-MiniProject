"""US-16 (FR-14): TC-09 compare models side by side."""
import pytest

from mlengine.models import Evaluation

pytestmark = pytest.mark.django_db


def run(client, ds, models):
    client.post(f"/evaluations/new/{ds.id}/", {"models": models})
    return list(Evaluation.objects.filter(dataset=ds).order_by("id"))


def test_compare_two_models_table_and_chart(auth_client, iris):  # TC-09
    a, b = run(auth_client, iris, ["logistic_regression", "random_forest"])
    page = auth_client.get(f"/evaluations/compare/?ids={a.id}&ids={b.id}")
    html = page.content.decode()
    assert page.status_code == 200
    assert "Logistic Regression" in html and "Random Forest" in html
    assert 'id="compare-chart"' in html and "vendor/chart.umd.js" in html
    assert f"{a.metrics['accuracy']:.3f}" in html and f"{b.metrics['accuracy']:.3f}" in html


def test_api_compare_values_match(auth_client, iris):
    a, b = run(auth_client, iris, ["knn", "svm"])
    data = auth_client.get(f"/api/evaluations/compare?ids={a.id},{b.id}").json()
    assert data["task_type"] == "classification"
    assert [c["key"] for c in data["columns"]] == ["accuracy", "precision", "recall", "f1"]
    assert data["rows"][0]["metrics"]["accuracy"] == a.metrics["accuracy"]
    assert data["best"]["accuracy"] in (a.id, b.id)


def test_selecting_one_model_shows_prompt(auth_client, iris):  # TC-09
    (a,) = run(auth_client, iris, ["knn"])
    page = auth_client.get(f"/evaluations/compare/?ids={a.id}")
    assert b"at least two" in page.content
    assert auth_client.get(f"/api/evaluations/compare?ids={a.id}").status_code == 400


def test_cannot_mix_classification_and_regression(auth_client, iris, diabetes):
    (a,) = run(auth_client, iris, ["knn"])
    (b,) = run(auth_client, diabetes, ["linear_regression"])
    page = auth_client.get(f"/evaluations/compare/?ids={a.id}&ids={b.id}")
    assert b"cannot be compared together" in page.content


def test_regression_compare_lower_is_better(auth_client, diabetes):
    a, b = run(auth_client, diabetes, ["linear_regression", "decision_tree_regressor"])
    data = auth_client.get(f"/api/evaluations/compare?ids={a.id},{b.id}").json()
    best_mae = min((a, b), key=lambda e: e.metrics["mae"]).id
    assert data["best"]["mae"] == best_mae


def test_other_users_evaluations_are_ignored(auth_client, iris, other_user, client):
    a, b = run(auth_client, iris, ["knn", "svm"])
    client.force_login(other_user)
    assert b"at least two" in client.get(f"/evaluations/compare/?ids={a.id}&ids={b.id}").content


def test_history_page_has_compare_controls(auth_client, iris):
    run(auth_client, iris, ["knn", "svm"])
    html = auth_client.get("/evaluations/").content.decode()
    assert "Compare selected" in html and 'name="ids"' in html
