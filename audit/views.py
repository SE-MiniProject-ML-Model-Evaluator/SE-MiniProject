"""Admin pages: user management (FR-17) and audit-log viewer (FR-18)."""
from datetime import datetime, time

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import AuditLog
from .permissions import admin_required
from .services import log_event

User = get_user_model()


def filter_log(params):
    qs = AuditLog.objects.select_related("user")
    if params.get("user"):
        qs = qs.filter(user_email__icontains=params["user"].strip())
    if params.get("action"):
        qs = qs.filter(action=params["action"])
    tz = timezone.get_current_timezone()
    for key, lookup, at in (("date_from", "timestamp__gte", time.min), ("date_to", "timestamp__lte", time.max)):
        value = params.get(key)
        if value:
            try:
                day = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                continue
            qs = qs.filter(**{lookup: timezone.make_aware(datetime.combine(day, at), tz)})
    return qs


@admin_required
def users(request):
    people = (User.objects.annotate(n_datasets=Count("datasets", distinct=True),
                                    n_evaluations=Count("evaluations", distinct=True))
              .order_by("-date_joined"))
    return render(request, "audit/users.html", {"people": people})


def _apply_user_action(request, target, action):
    """Shared by the page and the API. Returns an error message or None."""
    if target == request.user:
        return "You cannot change your own account here."
    if action == "deactivate":
        target.is_active = False
        target.save(update_fields=["is_active"])
        log_event("admin_deactivate", user=request.user, request=request, detail=target.email)
    elif action == "activate":
        target.is_active = True
        target.save(update_fields=["is_active"])
        log_event("admin_activate", user=request.user, request=request, detail=target.email)
    elif action == "make_admin":
        target.is_staff = True
        target.save(update_fields=["is_staff"])
        log_event("admin_promote", user=request.user, request=request, detail=target.email)
    elif action == "remove_admin":
        target.is_staff = False
        target.save(update_fields=["is_staff"])
        log_event("admin_demote", user=request.user, request=request, detail=target.email)
    elif action == "delete":
        email = target.email
        target.delete()          # cascades to the user's datasets (files removed) and evaluations
        log_event("admin_delete", user=request.user, request=request, detail=email)
    else:
        return "Unknown action."
    return None


@admin_required
@require_POST
def user_action(request, pk, action):
    target = get_object_or_404(User, pk=pk)
    email = target.email
    error = _apply_user_action(request, target, action)
    done = {"activate": "activated", "deactivate": "deactivated", "delete": "deleted",
            "make_admin": "is now an administrator", "remove_admin": "is no longer an administrator"}
    if error:
        messages.error(request, error)
    else:
        messages.success(request, f"{email} {done[action]}.")
    return redirect("/manage/users/")


@admin_required
def audit_log(request):
    entries = filter_log(request.GET)[:500]
    return render(request, "audit/audit_log.html", {
        "entries": entries, "actions": AuditLog.ACTIONS, "params": request.GET})
