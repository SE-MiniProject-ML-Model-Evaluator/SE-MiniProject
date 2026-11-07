"""GET /api/evaluations/compare?ids=1,2 (Design Spec 4.1 row 14)."""
from rest_framework.response import Response
from rest_framework.views import APIView

from mlme.errors import ApiError
from mlengine.models import Evaluation
from .services import CompareError, comparison
from .views import parse_ids


class CompareAPI(APIView):
    def get(self, request):
        ids = parse_ids(request.query_params.getlist("ids"))
        evaluations = list(Evaluation.objects.filter(owner=request.user, id__in=ids).select_related("dataset"))
        evaluations.sort(key=lambda e: ids.index(e.id))
        try:
            return Response(comparison(evaluations))
        except CompareError as exc:
            raise ApiError("VALIDATION_ERROR", str(exc))
