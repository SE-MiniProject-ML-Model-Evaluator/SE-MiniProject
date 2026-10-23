"""US-04 / SR-07: TC-21 (CSRF, XSS escaping, SQL injection)."""
import pytest
from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import Client

pytestmark = pytest.mark.django_db


def test_post_without_csrf_token_is_rejected():
    client = Client(enforce_csrf_checks=True)
    response = client.post("/accounts/login/", {"email": "a@b.com", "password": "x"})
    assert response.status_code == 403


def test_sql_injection_in_login_fails_safely(client):
    get_user_model().objects.create_user("real@test.com", "real@test.com", "Str0ngPass!")
    response = client.post("/accounts/login/", {"email": "real@test.com", "password": "' OR '1'='1"})
    assert response.status_code == 200
    assert "_auth_user_id" not in client.session


def test_templates_escape_user_content():
    html = Template("{{ name }}").render(Context({"name": "<script>alert(1)</script>"}))
    assert "<script>" not in html and "&lt;script&gt;" in html
