from django.contrib import admin
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone_number", "auth_type", "is_email_verified", "is_phone_verified")
    search_fields = ("username", "email", "phone_number")
    ordering = ("-created_at",)
