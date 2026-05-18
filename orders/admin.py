from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "total_price", "created_at")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "created_at")
    search_fields = ("order__user__username", "product__title")
    ordering = ("-created_at",)
