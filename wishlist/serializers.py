from rest_framework import serializers

from products.serializers import ProductSerializer
from wishlist.models import Wishlist, WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = WishlistItem
        fields = ("id", "product", "product_detail", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ("id", "user", "items", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")


class WishlistAddSerializer(serializers.Serializer):
    product = serializers.UUIDField()
