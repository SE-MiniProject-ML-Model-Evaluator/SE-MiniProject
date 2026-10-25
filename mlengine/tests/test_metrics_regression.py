"""US-14 (FR-13): TC-08 regression metrics."""
import pytest
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from mlengine.metrics import regression
from mlengine.models import Evaluation

pytestmark = pytest.mark.django_db


def test_compute_matches_scikit_learn():
    y_true, y_pred = [3.0, 5.0, 2.5, 7.0], [2.5, 5.0, 4.0, 8.0]
    m = regression.compute(y_true, y_pred)
    assert m["mae"] == round(mean_absolute_error(y_true, y_pred), 4)
    assert m["mse"] == round(mean_squared_error(y_true, y_pred), 4)
    assert m["r2"] == round(r2_score(y_true, y_pred), 4)


def test_regression_results_page_hides_classification_metrics(auth_client, diabetes):  # TC-08
    r = auth_client.post(f"/evaluations/new/{diabetes.id}/", {"models": ["linear_regression"]})
    evaluation = Evaluation.objects.get(dataset=diabetes)
    assert set(evaluation.metrics) == {"mae", "mse", "rmse", "r2"}
    assert 0 < evaluation.metrics["r2"] < 1
    page = auth_client.get(r["Location"]).content
    assert b"MAE" in page and b"MSE" in page and "R²".encode() in page
    assert b"Accuracy" not in page and b"Confusion matrix" not in page
