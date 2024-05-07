from distlib.compat import text_type
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
import after_response

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


account_activation_token = AccountActivationTokenGenerator()



@after_response.enable
def send_activation_email(request, user):
    """
    To send activation email to user
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    domain = get_current_site(request).domain
    link = reverse(
        "accounts_api:activate_account", kwargs={"uidb64": uidb64, "token": token}
    )
    activate_url = "http://" + domain + link

    # Define email subject
    subject = "Activate Your Account"
    # Render HTML content
    html_content = render_to_string(
        "email/activation_email.html",
        {
            "username": f"{user.email} {user.last_name}",
            "activate_url": activate_url,
        },
    )
    # Strip HTML tags to get plain text content
    text_content = strip_tags(html_content)

    # Create email message with subject and from/to emails
    email = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [user.email]
    )
    # Attach the HTML version
    email.attach_alternative(html_content, "text/html")
    # Send the email
    email.send()