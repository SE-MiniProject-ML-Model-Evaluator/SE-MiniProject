from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from accounts.permissions import get_owned_or_404
from datasets.models import Dataset
from .forms import TrainForm
from .jobs import start_evaluations
from .models import Evaluation


@login_required
def evaluation_list(request):
    evaluations = Evaluation.objects.filter(owner=request.user).select_related("dataset")[:200]
    return render(request, "mlengine/list.html", {"evaluations": evaluations})


@login_required
def train(request, dataset_id):
    dataset = get_owned_or_404(Dataset.objects.select_related("config"), request.user, dataset_id)
    if not dataset.is_configured:
        messages.error(request, "Configure the target and feature columns first.")
        return redirect(f"/datasets/{dataset.id}/configure/")
    form = TrainForm(request.POST if request.method == "POST" else None, task_type=dataset.config.task_type)
    if request.method == "POST" and form.is_valid():
        batch, _ = start_evaluations(request.user, dataset, form.cleaned_data["models"])
        return redirect(f"/evaluations/run/{batch}/")
    return render(request, "mlengine/train.html", {"dataset": dataset, "config": dataset.config, "form": form})


@login_required
def run_results(request, batch):
    evaluations = list(Evaluation.objects.filter(owner=request.user, batch=batch)
                       .select_related("dataset").order_by("id"))
    if not evaluations:
        raise Http404("Not found")
    return render(request, "mlengine/results.html", {
        "evaluations": evaluations, "dataset": evaluations[0].dataset,
        "pending": [e.id for e in evaluations if not e.is_done]})


@login_required
def evaluation_detail(request, pk):
    evaluation = get_owned_or_404(Evaluation.objects.select_related("dataset"), request.user, pk)
    return render(request, "mlengine/results.html", {
        "evaluations": [evaluation], "dataset": evaluation.dataset,
        "pending": [] if evaluation.is_done else [evaluation.id]})
