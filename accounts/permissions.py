"""SR-02 owner-only access helpers shared by the dataset and evaluation components."""
from django.http import Http404
from rest_framework.permissions import BasePermission


def get_owned_or_404(queryset, user, pk):
    """Return the object with this pk only if `user` owns it.

    Another user's object and a missing object give the same 404, so the
    existence of other users' data is never revealed (Design Spec 5.3, NOT_FOUND).
    """
    try:
        return queryset.get(pk=pk, owner=user)
    except (queryset.model.DoesNotExist, ValueError, TypeError):
        raise Http404("Not found")


class IsOwner(BasePermission):
    """DRF object-level permission: only the owner may access the object."""

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "owner_id", None) == request.user.id
