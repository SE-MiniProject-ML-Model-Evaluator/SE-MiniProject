"""US-17 (FR-15): TC-10 export evaluation report as PDF and CSV."""
import csv
import io

import pytest
from pypdf import PdfReader

from mlengine.models import Evaluation

pytestmark = pytest.mark.django_db


@pytest.fixture
def rf(auth_client, iris):
    auth_client.post(f"/evaluations/new/{iris.id}/",
                     {"models": ["random_forest"], "hp__random_forest__n_estimators": "50"})
    return Evaluation.objects.get()


def test_csv_report_contains_everything(auth_client, rf):  # TC-10
    r = auth_client.get(f"/api/evaluations/{rf.id}/report?format=csv")
    assert r.status_code == 200 and r["Content-Type"] == "text/csv"
    assert "attachment" in r["Content-Disposition"] and r["Content-Disposition"].endswith('.csv"')
    rows = list(csv.reader(io.StringIO(r.content.decode("utf-8-sig"))))
    fields = {row[0]: row[1] for row in rows if len(row) >= 2}
    assert fields["Dataset"] == "iris.csv" and fields["Model"] == "Random Forest"
    assert "n_estimators=50" in fields["Hyperparameters"]
    assert float(fields["Accuracy"]) == rf.metrics["accuracy"]
    assert any(row and row[0].startswith("confusion matrix") for row in rows)


def test_pdf_report_opens_and_contains_details(auth_client, rf):  # TC-10
    r = auth_client.get(f"/api/evaluations/{rf.id}/report?format=pdf")
    assert r.status_code == 200 and r["Content-Type"] == "application/pdf"
    assert r.content.startswith(b"%PDF")
    text = "".join(page.extract_text() for page in PdfReader(io.BytesIO(r.content)).pages)
    for expected in ("ML Model Evaluation Report", "iris.csv", "Random Forest", "n_estimators=50", "Accuracy",
                     "Confusion matrix"):
        assert expected in text


def test_regression_pdf(auth_client, diabetes):
    auth_client.post(f"/evaluations/new/{diabetes.id}/", {"models": ["linear_regression"]})
    e = Evaluation.objects.get()
    r = auth_client.get(f"/api/evaluations/{e.id}/report?format=pdf")
    text = "".join(p.extract_text() for p in PdfReader(io.BytesIO(r.content)).pages)
    assert "MAE" in text and "R2" in text and "Confusion" not in text


def test_bad_format_and_ownership(auth_client, rf, other_user, client):
    assert auth_client.get(f"/api/evaluations/{rf.id}/report?format=xls").status_code == 400
    client.force_login(other_user)
    assert client.get(f"/api/evaluations/{rf.id}/report?format=csv").status_code == 404


def test_results_page_has_download_buttons(auth_client, rf):
    html = auth_client.get(f"/evaluations/{rf.id}/").content.decode()
    assert f"/api/evaluations/{rf.id}/report?format=pdf" in html and "format=csv" in html
