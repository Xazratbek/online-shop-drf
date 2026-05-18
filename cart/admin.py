from django.contrib import admin
from cart.models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "created_at")
    search_fields = ("cart__user__username", "product__title")
    ordering = ("-created_at",)
