from django.contrib import admin

from .models import UserAddress


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "country", "city", "district", "is_default", "created_at")
    search_fields = ("user__username", "title", "country", "city", "district")
    ordering = ("-created_at",)
