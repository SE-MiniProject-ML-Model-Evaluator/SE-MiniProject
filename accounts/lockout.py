"""SR-05: lock an account for 15 minutes after 5 consecutive failed logins."""
import math
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from audit.services import log_event
from .models import LoginGuard

MAX_FAILED_LOGINS = 5
LOCK_MINUTES = 15


def _guard_for(email):
    user = get_user_model().objects.filter(username=email).first()
    if user is None:
        return None
    guard, _ = LoginGuard.objects.get_or_create(user=user)
    return guard


def minutes_left(email):
    """Minutes until the account unlocks, or 0 if it is not locked."""
    guard = _guard_for(email)
    if guard is None or not guard.is_locked:
        return 0
    return max(1, math.ceil((guard.locked_until - timezone.now()).total_seconds() / 60))


def record_failure(email, request=None):
    """Count a failed password for an existing account. Returns True if this failure locked it."""
    guard = _guard_for(email)
    if guard is None:
        return False
    guard.failed_logins += 1
    locked = guard.failed_logins >= MAX_FAILED_LOGINS
    if locked:
        guard.locked_until = timezone.now() + timedelta(minutes=LOCK_MINUTES)
        guard.failed_logins = 0
        log_event("account_locked", user=guard.user, request=request,
                  detail=f"{MAX_FAILED_LOGINS} failed logins; locked for {LOCK_MINUTES} min")
    guard.save()
    return locked


def record_success(user):
    # A single UPDATE (no read-then-write transaction) so concurrent logins don't hit SQLite lock errors
    LoginGuard.objects.filter(user=user).exclude(failed_logins=0, locked_until=None).update(
        failed_logins=0, locked_until=None)


def locked_message(minutes):
    return (f"This account is locked after {MAX_FAILED_LOGINS} failed login attempts. "
            f"Try again in {minutes} minute{'s' if minutes != 1 else ''}.")
