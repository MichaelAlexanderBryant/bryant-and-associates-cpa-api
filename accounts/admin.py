from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "first_name",
        "last_name",
        "email",
        "is_staff",
    ]
    fieldsets = ((None, {"fields": ("first_name","last_name", "email", "is_staff")}),)
    add_fieldsets = ((None, {"fields": ("first_name","last_name", "email", "password1", "password2")}),)

admin.site.register(CustomUser, CustomUserAdmin)
