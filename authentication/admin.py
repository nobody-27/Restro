from django.contrib import admin
from .models import User
# Register your models here.

admin.site.register(User)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    # You can add 'last_login' to list_display to see it in the list view as well
    list_display = ('username', 'email', 'first_name', 'last_name','last_login')

    # Define a new fieldset that includes last_login or add it to an existing one
    # fieldsets = BaseUserAdmin.fieldsets + (
        # (None, {'fields': ('last_login',)}),
    # )

    # Make last_login field read-only (optional)

# First, unregister the existing User model admin, then register the new UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
