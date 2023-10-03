# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registration_view, name="register"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
]
