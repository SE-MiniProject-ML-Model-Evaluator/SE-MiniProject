"""Model catalogue and evaluation REST endpoints (Design Spec 4.1, rows 9-12)."""
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import get_owned_or_404
from datasets.models import Dataset
from mlme.errors import ApiError
from .catalogue import CATALOGUE, InvalidModelConfig, public_catalogue
from .jobs import start_evaluations
from .models import Evaluation


class ModelCatalogueAPI(APIView):
    def get(self, request):
        return Response(public_catalogue())


class EvaluationListCreateAPI(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        qs = Evaluation.objects.filter(owner=request.user)
        if request.query_params.get("batch"):
            qs = qs.filter(batch=request.query_params["batch"])
        return Response([e.as_api() for e in qs[:200]])

    def post(self, request):
        dataset = get_owned_or_404(Dataset.objects.select_related("config"), request.user,
                                   request.data.get("dataset_id"))
        if not dataset.is_configured:
            raise ApiError("VALIDATION_ERROR", "Configure the dataset's target and features first.")
        model_key = request.data.get("model")
        if model_key not in CATALOGUE:
            raise ApiError("INVALID_MODEL_CONFIG", f"Unknown model '{model_key}'.", 422,
                           {"allowed": list(CATALOGUE)})
        if CATALOGUE[model_key]["task"] != dataset.config.task_type:
            raise ApiError("INVALID_MODEL_CONFIG",
                           f"'{model_key}' is not a {dataset.config.task_type} model.", 422)
        try:
            _, created = start_evaluations(request.user, dataset, [model_key],
                                           {model_key: request.data.get("hyperparameters") or {}})
        except InvalidModelConfig as exc:
            raise ApiError("INVALID_MODEL_CONFIG", str(exc), 422)
        evaluation = created[0]
        evaluation.refresh_from_db()
        return Response({"evaluation_id": evaluation.id, "status": evaluation.status},
                        status=status.HTTP_202_ACCEPTED)


class EvaluationDetailAPI(APIView):
    def get(self, request, pk):
        evaluation = get_owned_or_404(Evaluation.objects.all(), request.user, pk)
        return Response(evaluation.as_api())
