"""US-13 (FR-12): TC-07 classification metrics and confusion matrix."""
import pytest
from sklearn.metrics import accuracy_score, f1_score

from mlengine.metrics import classification
from mlengine.models import Evaluation

pytestmark = pytest.mark.django_db


def test_compute_matches_scikit_learn():
    y_true = ["a", "a", "b", "b", "c", "c"]
    y_pred = ["a", "b", "b", "b", "c", "a"]
    m = classification.compute(y_true, y_pred, ["a", "b", "c"])
    assert m["accuracy"] == round(accuracy_score(y_true, y_pred), 4)
    assert m["f1"] == round(f1_score(y_true, y_pred, average="weighted"), 4)
    assert m["confusion_matrix"] == [[1, 1, 0], [0, 2, 0], [1, 0, 1]]
    assert all(0 <= m[k] <= 1 for k in ("accuracy", "precision", "recall", "f1"))


def test_iris_results_page_shows_metrics_and_confusion_matrix(auth_client, iris):  # TC-07
    r = auth_client.post(f"/evaluations/new/{iris.id}/", {"models": ["logistic_regression", "random_forest"]})
    for e in Evaluation.objects.filter(dataset=iris):
        assert set(e.metrics) >= {"accuracy", "precision", "recall", "f1", "confusion_matrix"}
        assert e.metrics["accuracy"] > 0.8
        assert sum(map(sum, e.metrics["confusion_matrix"])) == e.test_rows
    page = auth_client.get(r["Location"]).content
    for text in (b"Accuracy", b"Precision", b"Recall", b"F1-score", b"Confusion matrix", b"virginica"):
        assert text in page


def test_api_returns_metrics_when_completed(auth_client, iris):
    r = auth_client.post("/api/evaluations", {"dataset_id": iris.id, "model": "svm"}, content_type="application/json")
    body = auth_client.get(f"/api/evaluations/{r.json()['evaluation_id']}").json()
    assert body["status"] == "completed" and 0 <= body["metrics"]["accuracy"] <= 1
