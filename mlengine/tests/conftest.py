import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from datasets.config import save_config
from datasets.services import store_dataset


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


def load(user, name):
    with open(f"sample_data/{name}", "rb") as fh:
        return store_dataset(user, SimpleUploadedFile(name, fh.read(), content_type="text/csv"))


@pytest.fixture
def iris(user):
    ds = load(user, "iris.csv")
    save_config(ds, {"target": "species", "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
                     "missing_strategy": "none", "test_size": 25, "random_seed": 42})
    ds.refresh_from_db()
    return ds


@pytest.fixture
def diabetes(user):
    ds = load(user, "diabetes.csv")
    save_config(ds, {"target": "disease_progression", "features": ["age", "sex", "bmi", "bp", "s1", "s5"],
                     "missing_strategy": "none", "test_size": 20, "random_seed": 42})
    ds.refresh_from_db()
    return ds
