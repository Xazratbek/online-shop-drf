from rest_framework import serializers

from cart.models import Cart, CartItem
from products.models import Product
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "product_detail", "quantity", "line_total", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")

    def get_line_total(self, obj):
        price = obj.product.discount_price or obj.product.price
        return price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "items", "total_price", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            total += (item.product.discount_price or item.product.price) * item.quantity
        return total


class AddCartItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        product = attrs["product"]
        quantity = attrs["quantity"]
        if product.stock < quantity:
            raise serializers.ValidationError({"quantity": "Omborda yetarli mahsulot yo'q"})
        return attrs


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
