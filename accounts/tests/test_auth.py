"""US-01 / US-02 / SR-01: TC-01, TC-02, TC-03, TC-17."""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()
pytestmark = pytest.mark.django_db


def register(client, email="user1@test.com", password="Str0ngPass!", confirm=None):
    return client.post("/accounts/register/", {"email": email, "password": password,
                                               "confirm_password": confirm or password})


def test_register_with_valid_details_creates_account(client):  # TC-01
    response = register(client)
    assert response.status_code == 302 and response["Location"] == "/accounts/login/"
    assert User.objects.filter(username="user1@test.com").exists()


def test_register_rejects_duplicate_email(client):  # TC-02
    register(client)
    response = register(client, email="USER1@test.com")
    assert response.status_code == 200
    assert b"already exists" in response.content
    assert User.objects.count() == 1


def test_register_rejects_short_password(client):  # TC-02
    response = register(client, email="new@test.com", password="abc12")
    assert response.status_code == 200
    assert not User.objects.filter(username="new@test.com").exists()


def test_password_is_stored_as_salted_pbkdf2_hash(client):  # TC-17 / SR-01
    register(client)
    user = User.objects.get(username="user1@test.com")
    assert user.password.startswith("pbkdf2_sha256$")
    assert "Str0ngPass!" not in user.password


def test_login_and_logout(client):  # TC-03
    register(client)
    response = client.post("/accounts/login/", {"email": "user1@test.com", "password": "Str0ngPass!"})
    assert response.status_code == 302 and response["Location"] == "/datasets/"
    assert "_auth_user_id" in client.session
    client.post("/accounts/logout/")
    assert "_auth_user_id" not in client.session


def test_login_with_wrong_password_shows_generic_error(client):  # TC-03
    register(client)
    response = client.post("/accounts/login/", {"email": "user1@test.com", "password": "wrong-pass"})
    assert response.status_code == 200
    assert b"Invalid email or password." in response.content


def test_logout_requires_post(client):
    assert client.get("/accounts/logout/").status_code == 405


def test_api_register_login_logout(client):
    r = client.post("/api/auth/register", {"email": "api@test.com", "password": "Str0ngPass!"},
                    content_type="application/json")
    assert r.status_code == 201 and r.json()["email"] == "api@test.com"
    r = client.post("/api/auth/register", {"email": "api@test.com", "password": "Str0ngPass!"},
                    content_type="application/json")
    assert r.status_code == 400 and r.json()["error"]["code"] == "EMAIL_ALREADY_EXISTS"
    r = client.post("/api/auth/login", {"email": "api@test.com", "password": "nope"},
                    content_type="application/json")
    assert r.status_code == 401 and r.json()["error"]["code"] == "AUTH_INVALID_CREDENTIALS"
    r = client.post("/api/auth/login", {"email": "api@test.com", "password": "Str0ngPass!"},
                    content_type="application/json")
    assert r.status_code == 200


def test_api_weak_password(client):
    r = client.post("/api/auth/register", {"email": "w@test.com", "password": "short"},
                    content_type="application/json")
    assert r.status_code == 400 and r.json()["error"]["code"] == "WEAK_PASSWORD"
