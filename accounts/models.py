"""Accounts use Django's built-in User model with the email address stored as the username (FR-01).

LoginGuard holds the lockout state from the USER entity in Design Spec 2.6 (SR-05).
"""
from django.conf import settings
from django.db import models
from django.utils import timezone


class LoginGuard(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="login_guard")
    failed_logins = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} failed={self.failed_logins} locked_until={self.locked_until}"

    @property
    def is_locked(self):
        return bool(self.locked_until and self.locked_until > timezone.now())
