"""US-21 (SR-05): TC-19 account lockout and session timeout."""
from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone

from accounts.models import LoginGuard
from audit.models import AuditLog

pytestmark = pytest.mark.django_db


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("a@test.com", "a@test.com", "Str0ngPass!")


def attempt(client, password):
    return client.post("/accounts/login/", {"email": "a@test.com", "password": password})


def test_five_failures_lock_the_account(client, user):  # TC-19 step 1-2
    for _ in range(4):
        assert b"Invalid email or password." in attempt(client, "wrong-pass").content
    r = attempt(client, "wrong-pass")
    assert b"locked" in r.content
    r = attempt(client, "Str0ngPass!")               # correct password refused while locked
    assert b"locked" in r.content and "_auth_user_id" not in client.session
    assert AuditLog.objects.filter(action="account_locked", user=user).exists()


def test_lock_expires_after_15_minutes(client, user):
    for _ in range(5):
        attempt(client, "wrong-pass")
    guard = LoginGuard.objects.get(user=user)
    assert timedelta(minutes=14) < guard.locked_until - timezone.now() <= timedelta(minutes=15)
    guard.locked_until = timezone.now() - timedelta(seconds=1)
    guard.save()
    attempt(client, "Str0ngPass!")
    assert "_auth_user_id" in client.session


def test_successful_login_resets_counter(client, user):
    for _ in range(3):
        attempt(client, "wrong-pass")
    attempt(client, "Str0ngPass!")
    assert LoginGuard.objects.get(user=user).failed_logins == 0


def test_api_returns_423_when_locked(client, user):
    for _ in range(4):
        client.post("/api/auth/login", {"email": "a@test.com", "password": "x"}, content_type="application/json")
    r = client.post("/api/auth/login", {"email": "a@test.com", "password": "x"}, content_type="application/json")
    assert r.status_code == 423 and r.json()["error"]["code"] == "ACCOUNT_LOCKED"
    r = client.post("/api/auth/login", {"email": "a@test.com", "password": "Str0ngPass!"},
                    content_type="application/json")
    assert r.status_code == 423


def test_unknown_email_does_not_crash(client):
    for _ in range(6):
        r = client.post("/accounts/login/", {"email": "nobody@test.com", "password": "x"})
    assert b"Invalid email or password." in r.content


def test_session_idle_timeout_is_30_minutes(client, user):  # TC-19 step 3
    assert settings.SESSION_COOKIE_AGE == 1800 and settings.SESSION_SAVE_EVERY_REQUEST
    attempt(client, "Str0ngPass!")
    assert client.get("/datasets/").status_code == 200
    Session.objects.update(expire_date=timezone.now() - timedelta(seconds=1))   # simulate 30 idle minutes
    r = client.get("/datasets/")
    assert r.status_code == 302 and r["Location"].startswith("/accounts/login/")


def test_admin_login_page_also_counts_failures(client, user):
    user.is_staff = True
    user.save()
    for _ in range(5):
        client.post("/accounts/admin-login/", {"email": "a@test.com", "password": "wrong-pass"})
    r = client.post("/accounts/admin-login/", {"email": "a@test.com", "password": "Str0ngPass!"})
    assert b"locked" in r.content and "_auth_user_id" not in client.session
