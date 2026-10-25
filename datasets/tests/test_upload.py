"""US-05 / US-06 / US-07: TC-04, TC-05, TC-18 (dataset part)."""
import pytest

from datasets.models import Dataset
from .conftest import csv_file, make_csv, sample_bytes

pytestmark = pytest.mark.django_db


def upload(client, f):
    return client.post("/datasets/upload/", {"file": f})


def test_upload_valid_csv_and_preview(auth_client, user):  # TC-04
    response = upload(auth_client, csv_file("iris.csv", sample_bytes("iris.csv")))
    dataset = Dataset.objects.get(owner=user)
    assert response.status_code == 302 and response["Location"] == f"/datasets/{dataset.id}/"
    assert (dataset.n_rows, dataset.n_cols) == (150, 5)
    assert {"name": "species", "type": "categorical"} in dataset.columns
    assert dataset.stored_name != "iris.csv" and dataset.path.exists()
    page = auth_client.get(f"/datasets/{dataset.id}/")
    assert page.status_code == 200 and page.content.count(b"<tr>") == 21   # header + 20 rows


@pytest.mark.parametrize("f, message", [
    (csv_file("data.csv", b"MZ\x90\x00binary-exe-content"), b"not a text CSV"),           # (a) exe renamed
    (csv_file("data.txt", make_csv()), b"Only .csv files"),
    (csv_file("data.csv", make_csv(cols=1)), b"at least 2 columns"),                       # (c)
    (csv_file("data.csv", make_csv(rows=10)), b"at least 20 data rows"),                    # (d)
    (csv_file("data.csv", b"1,2,3\n4,5,6\n" * 15), b"header row"),
    (csv_file("data.csv", make_csv(), content_type="image/png"), b"not CSV"),
])
def test_invalid_uploads_are_rejected_and_nothing_stored(auth_client, f, message):  # TC-05
    response = upload(auth_client, f)
    assert response.status_code == 200
    assert message in response.content
    assert Dataset.objects.count() == 0


def test_oversized_file_rejected(auth_client, settings):  # TC-05 (b)
    settings.MLME_MAX_UPLOAD_BYTES = 100
    response = upload(auth_client, csv_file("big.csv", make_csv()))
    assert b"50 MB" in response.content and Dataset.objects.count() == 0


def test_formula_cells_are_kept_as_plain_text(auth_client, user):  # TC-05 (e)
    content = make_csv().replace(b"c0,c1,c2\n", b"c0,c1,c2\n=cmd(),x,1\n")
    upload(auth_client, csv_file("f.csv", content))
    dataset = Dataset.objects.get(owner=user)
    page = auth_client.get(f"/datasets/{dataset.id}/")
    assert b"=cmd()" in page.content


def test_api_upload_returns_201_with_preview(auth_client):
    r = auth_client.post("/api/datasets", {"file": csv_file("iris.csv", sample_bytes("iris.csv"))})
    assert r.status_code == 201
    body = r.json()
    assert body["rows"] == 150 and len(body["preview"]) == 20
    assert auth_client.get(f"/api/datasets/{body['id']}/preview").json()["rows"][0]["species"] == "setosa"


def test_api_upload_errors_use_standard_format(auth_client):
    r = auth_client.post("/api/datasets", {"file": csv_file("x.csv", make_csv(rows=5))})
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "VALIDATION_ERROR" and "request_id" in r.json()["error"]


def test_pages_require_login(client):
    assert client.get("/datasets/")["Location"].startswith("/accounts/login/")
    assert client.get("/api/datasets").status_code in (401, 403)


def test_other_users_dataset_is_not_found(auth_client, other_user, client):  # TC-18 / SR-02
    auth_client.post("/datasets/upload/", {"file": csv_file("iris.csv", sample_bytes("iris.csv"))})
    dataset = Dataset.objects.get()
    client.force_login(other_user)
    assert client.get(f"/datasets/{dataset.id}/").status_code == 404
    assert client.get(f"/datasets/{dataset.id}/configure/").status_code == 404
    assert client.get(f"/api/datasets/{dataset.id}/preview").status_code == 404
    assert client.get("/api/datasets").json() == []
