"""Record logins, logouts, uploads and evaluation runs without touching the other components."""
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import log_event


@receiver(user_logged_in)
def on_login(sender, request, user, **kwargs):
    log_event("login_success", user=user, request=request)


@receiver(user_logged_out)
def on_logout(sender, request, user, **kwargs):
    if user is not None:
        log_event("logout", user=user, request=request)


@receiver(user_login_failed)
def on_login_failed(sender, credentials, request=None, **kwargs):
    log_event("login_failed", request=request, email=str(credentials.get("username", ""))[:254])


@receiver(post_save, sender="datasets.Dataset")
def on_upload(sender, instance, created, **kwargs):
    if created:
        log_event("upload", user=instance.owner,
                  detail=f"{instance.original_name} ({instance.n_rows} rows, {instance.n_cols} cols)")


@receiver(post_save, sender="mlengine.Evaluation")
def on_evaluation(sender, instance, created, **kwargs):
    if created:
        log_event("evaluation_run", user=instance.owner,
                  detail=f"{instance.model_label} on dataset #{instance.dataset_id}")
