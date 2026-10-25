"""Dataset REST endpoints (Design Spec 4.1, rows 4-7)."""
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import get_owned_or_404
from mlme.errors import ApiError
from .config import save_config
from .forms import ConfigForm
from .models import Dataset
from .services import preview, store_dataset
from .validation import UploadError


def _summary(dataset):
    return {"id": dataset.id, "name": dataset.original_name, "rows": dataset.n_rows,
            "columns": dataset.columns, "uploaded_at": dataset.uploaded_at.isoformat(),
            "configured": dataset.is_configured}


class DatasetListCreateAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        return Response([_summary(d) for d in Dataset.objects.filter(owner=request.user)])

    def post(self, request):
        uploaded = request.FILES.get("file")
        if uploaded is None:
            raise ApiError("VALIDATION_ERROR", "Send the CSV in the multipart field 'file'.")
        try:
            dataset = store_dataset(request.user, uploaded)
        except UploadError as err:
            raise ApiError(err.code, err.message, err.http_status, err.details)
        body = _summary(dataset)
        body["preview"] = preview(dataset)
        return Response(body, status=status.HTTP_201_CREATED)


class DatasetPreviewAPI(APIView):
    def get(self, request, pk):
        dataset = get_owned_or_404(Dataset.objects.all(), request.user, pk)
        return Response({"id": dataset.id, "columns": dataset.columns, "rows": preview(dataset)})


class DatasetConfigAPI(APIView):
    parser_classes = [JSONParser]

    def put(self, request, pk):
        dataset = get_owned_or_404(Dataset.objects.all(), request.user, pk)
        data = dict(request.data)
        test_size = data.get("test_size")
        if isinstance(test_size, (int, float)) and test_size <= 1:   # API accepts a fraction (0.25)
            data["test_size"] = test_size * 100
        form = ConfigForm(data, columns=dataset.column_names)
        if not form.is_valid():
            raise ApiError("VALIDATION_ERROR", "The configuration is invalid.", details=form.errors.get_json_data())
        config = save_config(dataset, form.cleaned_data)
        return Response({"dataset_id": dataset.id, "saved": True, "task_type": config.task_type})
