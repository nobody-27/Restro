from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils.encoding import force_str, force_bytes
from django.contrib.auth import get_user_model, login
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from authentication.utils import account_activation_token, send_activation_email
from authentication.models import User
from authentication.api.serializers import RegistrationSerializer

class RegistrationApiView(APIView):

    def post(self,request):

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()
            
            send_activation_email.after_response(request, user)

            return Response(
                {
                    "message": "User created successfully and an activation link has been sent to your email."
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class ActivateAccountView(APIView):
    """
    API endpoint to activate a user account.

    This view handles the activation process for user accounts. When a user clicks on
    the activation link sent to their email, this view is triggered to activate their
    account if the provided activation token is valid.

    Methods:
        - get: Activate user account based on provided UID and activation token.
    """

    def get(self, request, uidb64, token):
        """
        Activate user account based on provided UID and activation token.

        Args:
            request: HTTP request object.
            uidb64: Base64 encoded user ID.
            token: Activation token.

        Returns:
            Response: HTTP response indicating success or failure of the activation process.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(
                {"message": "Your account has been activated successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "The activation link is invalid or has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
