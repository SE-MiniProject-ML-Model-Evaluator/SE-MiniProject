from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/health", views.health, name="health"),
    path("django-admin/", admin.site.urls),
    # Each component owns its page and API routes (see each app's urls.py)
    path("", include("accounts.urls")),
    path("", include("datasets.urls")),
    path("", include("mlengine.urls")),
]
