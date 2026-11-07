"""Admin REST endpoints (Design Spec 4.1, rows 16-19)."""
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from mlme.errors import ApiError
from .permissions import IsAdmin
from .views import _apply_user_action, filter_log

User = get_user_model()


def _user_json(u):
    return {"id": u.id, "email": u.email, "role": "admin" if u.is_staff else "user", "is_active": u.is_active,
            "date_joined": u.date_joined.isoformat(), "datasets": getattr(u, "n_datasets", None),
            "evaluations": getattr(u, "n_evaluations", None)}


class AdminUserListAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        qs = User.objects.annotate(n_datasets=Count("datasets", distinct=True),
                                   n_evaluations=Count("evaluations", distinct=True)).order_by("id")
        return Response([_user_json(u) for u in qs])


class AdminUserDetailAPI(APIView):
    permission_classes = [IsAdmin]
    parser_classes = [JSONParser]

    def patch(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        actions = []
        if "is_active" in request.data:
            actions.append("activate" if request.data["is_active"] else "deactivate")
        if "is_admin" in request.data:
            actions.append("make_admin" if request.data["is_admin"] else "remove_admin")
        if not actions:
            raise ApiError("VALIDATION_ERROR", "Send {\"is_active\": true|false} and/or {\"is_admin\": true|false}.")
        for action in actions:
            error = _apply_user_action(request, target, action)
            if error:
                raise ApiError("VALIDATION_ERROR", error)
        return Response(_user_json(target))

    def delete(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        error = _apply_user_action(request, target, "delete")
        if error:
            raise ApiError("VALIDATION_ERROR", error)
        return Response(status=204)


class AuditLogAPI(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response([e.as_api() for e in filter_log(request.query_params)[:500]])
