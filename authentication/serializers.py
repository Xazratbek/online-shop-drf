from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import AuthType, User


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "auth_type", "password"]

    def validate(self, attrs):
        email = attrs.get("email")
        phone = attrs.get("phone_number")

        if not email and not phone:
            raise serializers.ValidationError("Email yoki phone_number kiriting.")
        if email and phone:
            raise serializers.ValidationError("Faqat email yoki phone_number dan bittasini yuboring.")

        attrs["auth_type"] = AuthType.EMAIL if email else AuthType.PHONE
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Username yoki parol noto'g'ri.")
        attrs["user"] = user
        return attrs
