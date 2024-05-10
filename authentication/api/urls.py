from django.urls import path
from authentication.api.views import *


app_name = "accounts_api"


urlpatterns = [
    path('registration/',RegistrationApiView.as_view(),name="registration"),
    path(
        "activate/<uidb64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate_account",
    ),
    path('login/',LoginApiView.as_view(),name="login")
]