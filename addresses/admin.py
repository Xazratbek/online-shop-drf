from django.contrib import admin
from addresses.models import UserAddress

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "country", "city", "is_default")
    search_fields = ("user__username", "title", "country", "city")
    ordering = ("-created_at",)
