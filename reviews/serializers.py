from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "user", "product", "rating", "title", "comment", "is_approved", "created_at", "updated_at")
        read_only_fields = ("id", "user", "is_approved", "created_at", "updated_at")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Reyting 1 dan 5 gacha bo'lishi kerak")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        product = attrs.get("product", getattr(self.instance, "product", None))
        if user and user.is_authenticated and product:
            queryset = Review.objects.filter(user=user, product=product)
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)
            if queryset.exists():
                raise serializers.ValidationError("Bu mahsulotga allaqachon sharh yozgansiz")
        return attrs
