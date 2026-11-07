"""Auth REST endpoints (Design Spec 4.1, rows 1-3)."""
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mlme.errors import ApiError
from audit.services import log_event
from .forms import RegisterForm
from .lockout import locked_message, minutes_left, record_failure, record_success


class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        data = {"email": request.data.get("email", ""), "password": request.data.get("password", ""),
                "confirm_password": request.data.get("password", "")}
        form = RegisterForm(data)
        if not form.is_valid():
            if "email" in form.errors and "already exists" in str(form.errors["email"]):
                raise ApiError("EMAIL_ALREADY_EXISTS", "An account with this email already exists.")
            if "password" in form.errors:
                raise ApiError("WEAK_PASSWORD", "Password must be at least 8 characters.",
                               details={"min_length": 8})
            raise ApiError("VALIDATION_ERROR", "Some fields are invalid.", details=form.errors.get_json_data())
        user = form.save()
        return Response({"id": user.id, "email": user.email, "role": "admin" if user.is_staff else "user"},
                        status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = str(request.data.get("email", "")).strip().lower()
        locked_for = minutes_left(email)
        if locked_for:
            log_event("login_failed", request=request, email=email, detail="account locked")
            raise ApiError("ACCOUNT_LOCKED", locked_message(locked_for), 423, {"retry_after_minutes": locked_for})
        user = authenticate(request, username=email, password=request.data.get("password", ""))
        if user is None:
            if record_failure(email, request):
                minutes = minutes_left(email)
                raise ApiError("ACCOUNT_LOCKED", locked_message(minutes), 423, {"retry_after_minutes": minutes})
            raise ApiError("AUTH_INVALID_CREDENTIALS", "Invalid email or password.", status.HTTP_401_UNAUTHORIZED)
        record_success(user)
        login(request, user)
        return Response({"id": user.id, "email": user.email})


class LogoutAPI(APIView):
    def post(self, request):
        logout(request)
        return Response({"logged_out": True})
