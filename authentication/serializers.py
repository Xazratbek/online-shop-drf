from rest_framework import serializers

class StartRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def validate(self, attrs):
        email = attrs.get("email")
        phone = attrs.get("phone_number")

        if not email and not phone:
            raise serializers.ValidationError(
                "Email yoki phone number kiritish majburiy"
            )

        if email and phone:
            raise serializers.ValidationError(
                "Faqat bittasi yuborilishi kerak"
            )

        return attrs

class VerifyOTPSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    code = serializers.CharField(max_length=6)

class CompleteProfileSerializer(serializers.Serializer):

    full_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    bio = serializers.CharField(required=False)

class UploadAvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField()