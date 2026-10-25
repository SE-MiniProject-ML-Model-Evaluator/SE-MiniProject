import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

SAMPLE = "sample_data/"


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("a@test.com", "a@test.com", "Str0ngPass!")


@pytest.fixture
def other_user(db):
    return get_user_model().objects.create_user("b@test.com", "b@test.com", "Str0ngPass!")


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client


def csv_file(name="data.csv", content=b"", content_type="text/csv"):
    return SimpleUploadedFile(name, content, content_type=content_type)


def sample_bytes(name):
    with open(SAMPLE + name, "rb") as fh:
        return fh.read()


def make_csv(rows=25, cols=3):
    header = ",".join(f"c{i}" for i in range(cols))
    body = "\n".join(",".join(str(r * cols + i) for i in range(cols)) for r in range(rows))
    return (header + "\n" + body + "\n").encode()
