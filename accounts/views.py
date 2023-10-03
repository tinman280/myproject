# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser

# Registration view
def registration_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your account"
            message = render_to_string(
                "/home/tinman/Documents/code/myproject/accounts/templates/registrations/activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse("Please check your email to activate your account.")
    else:
        form = CustomUserCreationForm()
    return render(request, "/home/tinman/Documents/code/myproject/accounts/templates/registrations/registraions.html", {"form": form})

# Activation view
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Account activated successfully!")
        else:
            return HttpResponse("Activation link is invalid!")
    except Exception as e:
        return HttpResponse(str(e))

# Login view
class CustomLoginView(LoginView):
    authentication_form = CustomUserLoginForm
    template_name = "/home/tinman/Documents/code/myproject/accounts/templates/registrations/login.html"


# OAuth Configuration
from oauthlib.oauth2 import WebApplicationClient

client_id = '109464848116-umfikhcaftdop221ad0dcpqo66i8142f.apps.googleusercontent.com'                 # Replace with your OAuth client ID
client_secret = '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'         # Replace with your OAuth client secret
redirect_uri = 'http://localhost:8000/accounts/oauth_callback/'  # Update with your actual callback URL
oauth_client = WebApplicationClient(client_id)

# Callback view for OAuth 2.0 authentication
def oauth_callback(request):
    if 'code' not in request.GET:
        return HttpResponse("OAuth callback failed: Missing authorization code.")

    authorization_code = request.GET['code']

    token_url = 'https://oauthprovider.com/token'  # Replace with the OAuth provider's token URL
    token_params = {
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
    }

    token_response = oauth_client.fetch_token(token_url, authorization_response=request.build_absolute_uri(), body=token_params)

    if 'access_token' not in token_response:
        return HttpResponse("OAuth callback failed: Unable to obtain access token.")

    user_info_url = 'https://oauthprovider.com/userinfo'  # Replace with the OAuth provider's user info URL
    user_info_response = oauth_client.get(user_info_url, headers={'Authorization': f'Bearer {token_response["access_token"]}'})

    if user_info_response.status_code != 200:
        return HttpResponse("OAuth callback failed: Unable to fetch user data.")

    user_data = user_info_response.json()

    try:
        user = CustomUser.objects.get(email=user_data['email'])
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create_user(email=user_data['email'], password=None)

    login(request, user)

    return redirect("/")  # Redirect to the homepage after successful login
