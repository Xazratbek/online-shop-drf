from django.contrib import admin

from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "rating", "is_approved", "created_at")
    search_fields = ("user__username", "product__title", "title", "comment")
    list_filter = ("rating", "is_approved")
    ordering = ("-created_at",)
