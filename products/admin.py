from django.contrib import admin
from products.models import Product, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "category", "price", "stock", "status")
    search_fields = ("title", "slug", "seller__username", "seller__email")
    list_filter = ("status", "category")
    ordering = ("-created_at",)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_main", "created_at")
    search_fields = ("product__title",)
    ordering = ("-created_at",)
