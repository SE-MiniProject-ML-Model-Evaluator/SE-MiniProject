from django.urls import path

from . import api, views

urlpatterns = [
    path("evaluations/", views.evaluation_list, name="evaluations"),
    path("evaluations/new/<int:dataset_id>/", views.train, name="train"),
    path("evaluations/run/<str:batch>/", views.run_results, name="run-results"),
    path("evaluations/<int:pk>/", views.evaluation_detail, name="evaluation-detail"),
    path("api/models", api.ModelCatalogueAPI.as_view(), name="api-models"),
    path("api/evaluations", api.EvaluationListCreateAPI.as_view(), name="api-evaluations"),
    path("api/evaluations/<int:pk>", api.EvaluationDetailAPI.as_view(), name="api-evaluation"),
]
