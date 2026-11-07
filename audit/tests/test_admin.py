"""US-19 (FR-17) and US-20 (FR-18, SR-08): TC-12, TC-18 admin part."""
import pytest

from audit.models import AuditLog
from datasets.models import Dataset

pytestmark = pytest.mark.django_db


def test_regular_user_cannot_open_admin_pages(client, user):  # TC-18
    client.force_login(user)
    assert client.get("/manage/users/").status_code == 403
    assert client.get("/manage/audit/").status_code == 403
    assert client.get("/api/admin/users").status_code == 403
    assert client.get("/api/admin/audit-log").status_code == 403


def test_admin_sees_users(client, admin_user, user):
    client.force_login(admin_user)
    page = client.get("/manage/users/")
    assert page.status_code == 200 and b"a@test.com" in page.content
    assert {u["email"] for u in client.get("/api/admin/users").json()} == {"a@test.com", "admin@test.com"}


def test_deactivated_user_cannot_log_in(client, admin_user, user):  # TC-12
    client.force_login(admin_user)
    client.post(f"/manage/users/{user.id}/deactivate/")
    user.refresh_from_db()
    assert user.is_active is False
    client.logout()
    r = client.post("/accounts/login/", {"email": "a@test.com", "password": "Str0ngPass!"})
    assert r.status_code == 200 and "_auth_user_id" not in client.session
    client.force_login(admin_user)
    client.post(f"/manage/users/{user.id}/activate/")
    user.refresh_from_db()
    assert user.is_active is True


def test_admin_delete_user_removes_their_data(client, admin_user, user, iris):
    path = iris.path
    client.force_login(admin_user)
    client.post(f"/manage/users/{user.id}/delete/")
    assert not Dataset.objects.exists() and not path.exists()


def test_admin_cannot_change_own_account(client, admin_user):
    client.force_login(admin_user)
    client.post(f"/manage/users/{admin_user.id}/deactivate/")
    admin_user.refresh_from_db()
    assert admin_user.is_active


def test_api_patch_and_delete_user(client, admin_user, user):
    client.force_login(admin_user)
    r = client.patch(f"/api/admin/users/{user.id}", {"is_active": False}, content_type="application/json")
    assert r.status_code == 200 and r.json()["is_active"] is False
    assert client.delete(f"/api/admin/users/{user.id}").status_code == 204


def test_audit_log_records_login_upload_run_and_admin_actions(client, admin_user, user, iris):  # TC-12 / SR-08
    client.post("/accounts/login/", {"email": "a@test.com", "password": "wrong-password"})
    client.post("/accounts/login/", {"email": "a@test.com", "password": "Str0ngPass!"})
    client.post(f"/evaluations/new/{iris.id}/", {"models": ["knn"]})
    client.post("/accounts/logout/")
    client.force_login(admin_user)
    client.post(f"/manage/users/{user.id}/deactivate/")
    actions = set(AuditLog.objects.values_list("action", flat=True))
    assert {"login_failed", "login_success", "upload", "evaluation_run", "logout", "admin_deactivate"} <= actions
    entry = AuditLog.objects.filter(action="login_success", user_email="a@test.com").first()
    assert entry.user == user and entry.ip_address == "127.0.0.1" and entry.timestamp
    assert not AuditLog.objects.filter(detail__icontains="Str0ngPass!").exists()   # no passwords logged


def test_audit_log_page_and_filters(client, admin_user, user, iris):
    client.force_login(admin_user)
    page = client.get("/manage/audit/?user=a@test.com&action=upload")
    assert page.status_code == 200 and b"iris.csv" in page.content
    data = client.get("/api/admin/audit-log?action=upload").json()
    assert len(data) == 1 and data[0]["user_email"] == "a@test.com"
    assert client.get("/api/admin/audit-log?date_from=2999-01-01").json() == []


def test_admin_login_page_lets_admins_in(client, admin_user):
    page = client.get("/accounts/admin-login/")
    assert page.status_code == 200 and b"Administrator login" in page.content
    r = client.post("/accounts/admin-login/", {"email": "admin@test.com", "password": "Str0ngPass!"})
    assert r.status_code == 302 and r["Location"] == "/manage/users/"
    assert client.get("/manage/users/").status_code == 200


def test_admin_login_page_refuses_regular_users(client, user):
    r = client.post("/accounts/admin-login/", {"email": "a@test.com", "password": "Str0ngPass!"})
    assert r.status_code == 200 and b"not an administrator" in r.content
    assert "_auth_user_id" not in client.session


def test_login_pages_link_to_each_other(client):
    assert b"/accounts/admin-login/" in client.get("/accounts/login/").content
    assert b"/accounts/login/" in client.get("/accounts/admin-login/").content


def test_make_and_remove_admin(client, admin_user, user):
    client.force_login(admin_user)
    client.post(f"/manage/users/{user.id}/make_admin/")
    user.refresh_from_db()
    assert user.is_staff
    assert AuditLog.objects.filter(action="admin_promote", detail="a@test.com").exists()
    client.post(f"/manage/users/{user.id}/remove_admin/")
    user.refresh_from_db()
    assert not user.is_staff
    r = client.patch(f"/api/admin/users/{user.id}", {"is_admin": True}, content_type="application/json")
    assert r.status_code == 200 and r.json()["role"] == "admin"


def test_admin_cannot_remove_own_admin_rights(client, admin_user):
    client.force_login(admin_user)
    client.post(f"/manage/users/{admin_user.id}/remove_admin/")
    admin_user.refresh_from_db()
    assert admin_user.is_staff
