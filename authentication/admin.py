from django.contrib import admin

from .models import OTPCode, RegistrationSession


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "purpose", "email", "phone_number", "is_used", "expires_at", "created_at")
    search_fields = ("code", "email", "phone_number")
    ordering = ("-created_at",)


@admin.register(RegistrationSession)
class RegistrationSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "current_step", "is_completed", "created_at")
    search_fields = ("user__username", "user__email", "user__phone_number")
    ordering = ("-created_at",)
