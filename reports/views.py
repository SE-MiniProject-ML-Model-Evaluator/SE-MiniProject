"""Compare page (FR-14) and report downloads (FR-15)."""
import logging
import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from accounts.permissions import get_owned_or_404
from mlengine.models import Evaluation
from .services import CompareError, comparison, report_csv, report_pdf

logger = logging.getLogger(__name__)


def parse_ids(raw_values):
    ids = []
    for raw in raw_values:
        for part in str(raw).split(","):
            if part.strip().isdigit():
                ids.append(int(part))
    return list(dict.fromkeys(ids))      # keep order, drop duplicates


@login_required
def compare(request):
    ids = parse_ids(request.GET.getlist("ids"))
    evaluations = list(Evaluation.objects.filter(owner=request.user, id__in=ids).select_related("dataset"))
    evaluations.sort(key=lambda e: ids.index(e.id))
    context = {"evaluations": evaluations}
    try:
        context["data"] = comparison(evaluations)
    except CompareError as exc:
        context["error"] = str(exc)
    return render(request, "reports/compare.html", context)


def _filename(evaluation, ext):
    base = re.sub(r"[^A-Za-z0-9]+", "_", f"{evaluation.model_label}_{evaluation.dataset.original_name}").strip("_")
    return f"report_{evaluation.id}_{base}.{ext}"


@login_required
def report(request, pk):
    """GET /api/evaluations/{id}/report?format=pdf|csv (Design Spec 4.1 row 15)."""
    evaluation = get_owned_or_404(Evaluation.objects.select_related("dataset__config"), request.user, pk)
    if evaluation.status != "completed":
        return HttpResponse("Only completed evaluations can be exported.", status=400, content_type="text/plain")
    fmt = request.GET.get("format", "pdf").lower()
    if fmt == "csv":
        content, ctype = report_csv(evaluation), "text/csv"
    elif fmt == "pdf":
        try:
            content, ctype = report_pdf(evaluation), "application/pdf"
        except Exception:   # Design Spec 5.4: PDF failure -> 500, CSV still available
            logger.exception("PDF report failed for evaluation %s", pk)
            return HttpResponse("The PDF could not be generated. Try the CSV export.", status=500,
                                content_type="text/plain")
    else:
        return HttpResponse("format must be pdf or csv.", status=400, content_type="text/plain")
    response = HttpResponse(content, content_type=ctype)
    response["Content-Disposition"] = f'attachment; filename="{_filename(evaluation, fmt)}"'
    return response
