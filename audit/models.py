"""AUDIT_LOG entity (Design Spec 2.6) for SR-08 / FR-18."""
from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    ACTIONS = [
        ("login_success", "Login"),
        ("login_failed", "Failed login"),
        ("logout", "Logout"),
        ("account_locked", "Account locked"),
        ("upload", "Dataset upload"),
        ("dataset_delete", "Dataset deleted"),
        ("evaluation_run", "Evaluation run"),
        ("evaluation_delete", "Evaluation deleted"),
        ("admin_activate", "Admin: user activated"),
        ("admin_deactivate", "Admin: user deactivated"),
        ("admin_delete", "Admin: user deleted"),
        ("admin_promote", "Admin: made administrator"),
        ("admin_demote", "Admin: administrator removed"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="audit_entries")
    user_email = models.CharField(max_length=254, blank=True)    # kept even if the user is deleted
    action = models.CharField(max_length=32, choices=ACTIONS, db_index=True)
    detail = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp", "-id"]

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d %H:%M} {self.user_email or '-'} {self.action}"

    def as_api(self):
        return {"id": self.id, "timestamp": self.timestamp.isoformat(), "user_id": self.user_id,
                "user_email": self.user_email, "action": self.action, "detail": self.detail,
                "ip_address": self.ip_address}
