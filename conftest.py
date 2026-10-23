import pytest


@pytest.fixture(autouse=True)
def _test_settings(settings, tmp_path):
    """Run training jobs synchronously and store uploads in a temp folder during tests."""
    settings.MLME_SYNC_JOBS = True
    settings.MEDIA_ROOT = tmp_path / "media"
