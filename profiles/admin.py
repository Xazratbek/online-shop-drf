from django.contrib import admin

from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "shop_name", "is_verified_seller", "gender", "preferred_language", "created_at")
    search_fields = ("user__username", "user__email", "user__phone_number")
    list_filter = ("role", "is_verified_seller", "gender", "preferred_language")
    ordering = ("-created_at",)
