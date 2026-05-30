from rest_framework import serializers

from products.models import Product, ProductImage, Status


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "product", "image", "is_main", "created_at", "updated_at")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "seller",
            "category",
            "title",
            "slug",
            "description",
            "price",
            "discount_price",
            "final_price",
            "stock",
            "status",
            "images",
            "created_at",
            "updated_at",
        )

    def get_final_price(self, obj):
        return obj.discount_price or obj.price

    def validate(self, attrs):
        discount_price = attrs.get("discount_price", getattr(self.instance, "discount_price", None))
        price = attrs.get("price", getattr(self.instance, "price", None))
        if discount_price is not None and price is not None and discount_price > price:
            raise serializers.ValidationError({"discount_price": "Chegirma narxi asosiy narxdan katta bo'lmasin"})
        return attrs


class ProductStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Status.choices)
