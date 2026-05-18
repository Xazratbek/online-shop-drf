from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "auth_type",
            "is_email_verified",
            "is_phone_verified",
            "avatar",
            "bio",
            "created_at",
        ]
