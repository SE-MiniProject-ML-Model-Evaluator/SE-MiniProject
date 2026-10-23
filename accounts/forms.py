from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterForm(forms.Form):
    """FR-01: unique email + password of at least 8 characters."""
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, help_text="At least 8 characters.")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password)
        return password

    def clean(self):
        data = super().clean()
        if data.get("password") and data.get("password") != data.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match.")
        return data

    def save(self):
        email = self.cleaned_data["email"]
        # create_user hashes the password with PBKDF2 (SR-01); the plaintext is never stored or logged
        return User.objects.create_user(username=email, email=email, password=self.cleaned_data["password"])


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
