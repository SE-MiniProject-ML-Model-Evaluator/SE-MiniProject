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


NOT_ADMIN = "This account is not an administrator. Use the normal Log in page."


def login_view(request, admin=False):
    """FR-02 login. With admin=True (the "Admin login" page) only administrators may sign in."""
    if request.user.is_authenticated:
        return redirect("/manage/users/" if admin and request.user.is_staff else "/datasets/")
    form = LoginForm(request.POST if request.method == "POST" else None)
    error = None
    if request.method == "POST" and form.is_valid():
        user = authenticate(request, username=form.cleaned_data["email"].strip().lower(),
                            password=form.cleaned_data["password"])
        if user is not None and admin and not user.is_staff:
            error = NOT_ADMIN
        elif user is not None:
            login(request, user)
            next_url = request.GET.get("next", "")
            safe = next_url.startswith("/") and not next_url.startswith("//")
            return redirect(next_url if safe else ("/manage/users/" if admin else "/datasets/"))
        else:
            error = "Invalid email or password."   # generic: no user enumeration
    return render(request, "accounts/login.html", {"form": form, "error": error, "admin": admin})


def admin_login_view(request):
    """Administrator sign-in page (FR-17): same checks as login, but only staff accounts get in."""
    return login_view(request, admin=True)


@require_POST
def logout_view(request):
    """FR-02: ends the session immediately (POST only, protected by CSRF)."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/accounts/login/")
