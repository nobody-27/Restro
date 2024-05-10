from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from authentication.managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user account.

    Attributes:
        email (EmailField): The email address of the user. Used as the username for authentication.
        username (EmailField): The username of the user (optional).
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        is_staff (BooleanField): Indicates whether the user has staff permissions.
        is_superuser (BooleanField): Indicates whether the user has superuser permissions.
        is_active (BooleanField): Indicates whether the user account is active.
        last_login (DateTimeField): The timestamp of the user's last login.
        date_joined (DateTimeField): The timestamp of when the user account was created.
        date_of_birth (DateField): The date of birth of the user (optional).
        
    Manager:
        objects (UserManager): Manager for managing user accounts.

    """

    email = models.EmailField(_("Email ID"), max_length=254, unique=True)
    username = models.EmailField(
        _("Username"), max_length=254, unique=True, null=True, blank=True
    )
    first_name = models.CharField(
        _("First Name"), max_length=150, null=True, blank=False
    )
    last_name = models.CharField(_("Last Name"), max_length=150, null=True, blank=False)
    is_staff = models.BooleanField(_("Staff Status"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    is_active = models.BooleanField(_("Active"), default=False)
    last_login = models.DateTimeField(
        _("Last Login"), auto_now=True, null=True, blank=True
    )
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_email(self):
        """
        Get the email address of the user.

        Returns:
            str: The email address of the user.
        """
        return self.email

    def get_full_name(self):
        """
        Get the full name of the user.

        Returns:
            str: The full name of the user.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def __str__(self):
        """
        Get the string representation of the user.

        Returns:
            str: The email address of the user.
        """
        return self.email



        
