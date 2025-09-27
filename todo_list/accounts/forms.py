from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

def validate_password_strength(value):
    errors = []
    if len(value) < 8:
        errors.append("At least 8 characters.")
    if not re.search(r"[A-Z]", value):
        errors.append("At least one uppercase letter.")
    if not re.search(r"\d", value):
        errors.append("At least one number.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>£]', value):
        errors.append("At least one special/punctuation character.")
    if errors:
        raise ValidationError(errors)
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required")
    # override password1 to attach server-side validator
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        validators=[validate_password_strength],
        help_text="Min 8 characters. At least one of each: uppercase, number, punctuation."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email").lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

