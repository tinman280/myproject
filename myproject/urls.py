# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from accounts.views import oauth_callback  # Import the OAuth callback view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/oauth_callback/", oauth_callback, name="oauth_callback"),  # Add the OAuth callback URL
]
