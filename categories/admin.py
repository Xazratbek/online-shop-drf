from django.contrib import admin
from categories.models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "created_at")
    search_fields = ("name", "slug")
    ordering = ("name",)
