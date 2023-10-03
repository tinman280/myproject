# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username")

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password")
