from rest_framework import serializers

from addresses.models import UserAddress


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserAddress
        fields = (
            "id",
            "user",
            "title",
            "country",
            "city",
            "district",
            "address",
            "latitude",
            "longitude",
            "is_default",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")
