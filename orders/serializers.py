from rest_framework import serializers

from orders.models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "product_detail", "quantity", "price", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "user", "status", "total_price", "items", "created_at", "updated_at")
        read_only_fields = ("id", "user", "status", "total_price", "created_at", "updated_at")
