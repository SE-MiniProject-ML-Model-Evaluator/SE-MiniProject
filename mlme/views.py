from django.http import JsonResponse
from django.shortcuts import redirect, render


def health(request):
    """GET /api/health - liveness check used by CI and deployment."""
    return JsonResponse({"status": "ok"})


def home(request):
    if request.user.is_authenticated:
        return redirect("/datasets/")
    return render(request, "home.html")
