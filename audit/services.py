"""C10 audit service: one function to record a security-relevant event (SR-08).

Never pass passwords or dataset contents in `detail`.
"""
from .models import AuditLog


def client_ip(request):
    if request is None:
        return None
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    ip = forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")
    return ip or None


def log_event(action, user=None, request=None, detail="", email=""):
    if user is not None and not getattr(user, "is_authenticated", False):
        user = None
    return AuditLog.objects.create(
        action=action, user=user, user_email=(user.email if user else email)[:254],
        detail=str(detail)[:500], ip_address=client_ip(request))
