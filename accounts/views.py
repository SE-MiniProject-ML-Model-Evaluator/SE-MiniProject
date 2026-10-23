from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("/datasets/")
    form = RegisterForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created. Please log in.")
        return redirect("/accounts/login/")
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/datasets/")
    form = LoginForm(request.POST if request.method == "POST" else None)
    error = None
    if request.method == "POST" and form.is_valid():
        user = authenticate(request, username=form.cleaned_data["email"].strip().lower(),
                            password=form.cleaned_data["password"])
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "")
            return redirect(next_url if next_url.startswith("/") and not next_url.startswith("//") else "/datasets/")
        error = "Invalid email or password."   # generic: no user enumeration
    return render(request, "accounts/login.html", {"form": form, "error": error})


@require_POST
def logout_view(request):
    """FR-02: ends the session immediately (POST only, protected by CSRF)."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/accounts/login/")
