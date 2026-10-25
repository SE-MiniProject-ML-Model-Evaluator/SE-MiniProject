from django.urls import path

from . import api, views

urlpatterns = [
    path("datasets/", views.dashboard, name="dashboard"),
    path("datasets/upload/", views.upload, name="upload"),
    path("datasets/<int:pk>/", views.detail, name="dataset-detail"),
    path("datasets/<int:pk>/configure/", views.configure, name="dataset-configure"),
    path("api/datasets", api.DatasetListCreateAPI.as_view(), name="api-datasets"),
    path("api/datasets/<int:pk>/preview", api.DatasetPreviewAPI.as_view(), name="api-dataset-preview"),
    path("api/datasets/<int:pk>/config", api.DatasetConfigAPI.as_view(), name="api-dataset-config"),
]
