from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Rôle & centre", {"fields": ("role", "centre")}),
    )

    list_display = ("username", "email", "role", "centre", "is_staff", "is_active")
    list_filter = ("role", "centre", "is_staff", "is_active")
