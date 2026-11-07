"""Remove a dataset's stored file when its record is deleted (FR-16, data retention)."""
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Dataset


@receiver(post_delete, sender=Dataset)
def remove_file(sender, instance, **kwargs):
    try:
        instance.path.unlink(missing_ok=True)
    except OSError:
        pass
