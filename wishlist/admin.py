from django.contrib import admin

from wishlist.models import Wishlist, WishlistItem


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("wishlist", "product", "created_at")
    search_fields = ("wishlist__user__username", "product__title")
    ordering = ("-created_at",)
