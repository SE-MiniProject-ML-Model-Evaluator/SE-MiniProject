import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from datasets.config import save_config
from datasets.services import store_dataset

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user("a@test.com", "a@test.com", "Str0ngPass!")


@pytest.fixture
def admin_user(db):
    return User.objects.create_user("admin@test.com", "admin@test.com", "Str0ngPass!", is_staff=True)


@pytest.fixture
def iris(user):
    with open("sample_data/iris.csv", "rb") as fh:
        ds = store_dataset(user, SimpleUploadedFile("iris.csv", fh.read(), content_type="text/csv"))
    save_config(ds, {"target": "species", "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
                     "missing_strategy": "none", "test_size": 25, "random_seed": 42})
    ds.refresh_from_db()
    return ds
