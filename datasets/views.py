from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.permissions import get_owned_or_404
from .config import initial_from, save_config
from .forms import ConfigForm, UploadForm
from .models import Dataset
from .services import preview, store_dataset
from .validation import UploadError


@login_required
def dashboard(request):
    datasets = Dataset.objects.filter(owner=request.user).select_related("config")
    return render(request, "datasets/dashboard.html", {"datasets": datasets})


@login_required
def upload(request):
    posted = request.method == "POST"
    form = UploadForm(request.POST if posted else None, request.FILES if posted else None)
    if request.method == "POST" and form.is_valid():
        try:
            dataset = store_dataset(request.user, form.cleaned_data["file"])
        except UploadError as err:
            form.add_error("file", err.message)
        else:
            messages.success(request, f"Uploaded {dataset.original_name}: "
                                      f"{dataset.n_rows} rows, {dataset.n_cols} columns.")
            return redirect(f"/datasets/{dataset.id}/")
    return render(request, "datasets/upload.html", {"form": form})


@login_required
def detail(request, pk):
    dataset = get_owned_or_404(Dataset.objects.all(), request.user, pk)
    rows = preview(dataset)
    return render(request, "datasets/preview.html", {"dataset": dataset, "rows": rows,
                                                     "columns": dataset.column_names})


@login_required
def configure(request, pk):
    dataset = get_owned_or_404(Dataset.objects.all(), request.user, pk)
    form = ConfigForm(request.POST if request.method == "POST" else None, columns=dataset.column_names,
                      initial=initial_from(dataset))
    if request.method == "POST" and form.is_valid():
        config = save_config(dataset, form.cleaned_data)
        messages.success(request, f"Configuration saved. Detected task: {config.task_type}.")
        return redirect(f"/evaluations/new/{dataset.id}/")
    return render(request, "datasets/configure.html", {"dataset": dataset, "form": form})
