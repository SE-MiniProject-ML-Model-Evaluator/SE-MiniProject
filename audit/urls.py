from django.urls import path

from . import api, views

urlpatterns = [
    path("manage/users/", views.users, name="admin-users"),
    path("manage/users/<int:pk>/<str:action>/", views.user_action, name="admin-user-action"),
    path("manage/audit/", views.audit_log, name="admin-audit"),
    path("api/admin/users", api.AdminUserListAPI.as_view(), name="api-admin-users"),
    path("api/admin/users/<int:pk>", api.AdminUserDetailAPI.as_view(), name="api-admin-user"),
    path("api/admin/audit-log", api.AuditLogAPI.as_view(), name="api-admin-audit"),
]
