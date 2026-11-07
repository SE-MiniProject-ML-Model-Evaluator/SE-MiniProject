"""US-22 (SR-06): TC-20 at most 100 API requests per minute per user."""
import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


def test_101st_request_in_a_minute_gets_429(client):  # TC-20
    user = get_user_model().objects.create_user("a@test.com", "a@test.com", "Str0ngPass!")
    client.force_login(user)
    codes = [client.get("/api/datasets").status_code for _ in range(150)]
    assert codes[:100] == [200] * 100
    assert set(codes[100:]) == {429}
    r = client.get("/api/datasets")
    assert r.json()["error"]["code"] == "RATE_LIMITED" and int(r["Retry-After"]) > 0


def test_limit_is_per_user(client):
    User = get_user_model()
    a = User.objects.create_user("a@test.com", "a@test.com", "Str0ngPass!")
    b = User.objects.create_user("b@test.com", "b@test.com", "Str0ngPass!")
    client.force_login(a)
    for _ in range(101):
        client.get("/api/datasets")
    client.force_login(b)
    assert client.get("/api/datasets").status_code == 200
