from django.urls import path

from . import api, views

urlpatterns = [
    path("evaluations/compare/", views.compare, name="compare"),
    path("api/evaluations/compare", api.CompareAPI.as_view(), name="api-compare"),
    path("api/evaluations/<int:pk>/report", views.report, name="api-report"),
]
