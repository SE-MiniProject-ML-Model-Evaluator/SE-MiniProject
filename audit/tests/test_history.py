"""US-18 (FR-16): TC-11 evaluation history - view and delete."""
import pytest

from datasets.models import Dataset
from mlengine.models import Evaluation

pytestmark = pytest.mark.django_db


def test_history_lists_own_evaluations(client, user, iris):
    client.force_login(user)
    client.post(f"/evaluations/new/{iris.id}/", {"models": ["knn", "decision_tree", "svm"]})
    page = client.get("/evaluations/")
    assert page.status_code == 200
    for label in (b"k-Nearest Neighbours", b"Decision Tree", b"Support Vector Machine"):
        assert label in page.content


def test_delete_evaluation(client, user, iris):  # TC-11
    client.force_login(user)
    client.post(f"/evaluations/new/{iris.id}/", {"models": ["knn", "svm"]})
    target = Evaluation.objects.filter(dataset=iris).first()
    r = client.post(f"/evaluations/{target.id}/delete/")
    assert r.status_code == 302
    assert not Evaluation.objects.filter(pk=target.pk).exists()
    assert client.get(f"/evaluations/{target.id}/").status_code == 404
    assert Evaluation.objects.filter(dataset=iris).count() == 1


def test_delete_requires_post(client, user, iris):
    client.force_login(user)
    client.post(f"/evaluations/new/{iris.id}/", {"models": ["knn"]})
    e = Evaluation.objects.get()
    assert client.get(f"/evaluations/{e.id}/delete/").status_code == 405


def test_delete_dataset_removes_file_and_evaluations(client, user, iris):
    client.force_login(user)
    client.post(f"/evaluations/new/{iris.id}/", {"models": ["knn"]})
    path = iris.path
    assert path.exists()
    client.post(f"/datasets/{iris.id}/delete/")
    assert not Dataset.objects.filter(pk=iris.pk).exists()
    assert not path.exists()
    assert Evaluation.objects.count() == 0


def test_api_delete(client, user, iris):
    client.force_login(user)
    r = client.post("/api/evaluations", {"dataset_id": iris.id, "model": "knn"}, content_type="application/json")
    eid = r.json()["evaluation_id"]
    assert client.delete(f"/api/evaluations/{eid}").status_code == 204
    assert client.get(f"/api/evaluations/{eid}").status_code == 404
    assert client.delete(f"/api/datasets/{iris.id}").status_code == 204
    assert client.get("/api/datasets").json() == []


def test_cannot_delete_other_users_data(client, iris, admin_user):
    client.force_login(admin_user)   # even an admin cannot delete another user's dataset via these routes
    assert client.post(f"/datasets/{iris.id}/delete/").status_code == 404
    assert Dataset.objects.filter(pk=iris.pk).exists()
