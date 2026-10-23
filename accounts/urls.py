from django.urls import path

from . import api, views

urlpatterns = [
    path("accounts/register/", views.register_view, name="register"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("api/auth/register", api.RegisterAPI.as_view(), name="api-register"),
    path("api/auth/login", api.LoginAPI.as_view(), name="api-login"),
    path("api/auth/logout", api.LogoutAPI.as_view(), name="api-logout"),
]
