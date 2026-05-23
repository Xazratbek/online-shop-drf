from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.db.models import Q
from accounts.models import User
from authentication.models import OTPCode, Purpose, RegistrationSession


class StartRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def validate(self, attrs):
        email = attrs.get("email")
        phone = attrs.get("phone_number")

        if not email and not phone:
            raise serializers.ValidationError("Email yoki phone number kiritish majburiy")
        if email and phone:
            raise serializers.ValidationError("Faqat bittasi yuborilishi kerak")

        return attrs


class VerifyOTPSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    code = serializers.CharField(max_length=6)

class CompleteProfileSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    full_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu username band")
        return value


class UploadAvatarSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    avatar = serializers.ImageField(required=False, allow_null=True)


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login = attrs.get("login")
        password = attrs.get("password")
        user_obj = User.objects.filter(
            Q(username=login) | Q(email=login) | Q(phone_number=login)
        ).first()
        if user_obj:
            user = authenticate(username=user_obj.username, password=password)
        else:
            user = None
        if not user:
            raise serializers.ValidationError("Login yoki parol noto'g'ri")
        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "bio", "avatar")


class RegistrationSessionSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = RegistrationSession
        fields = ("id", "current_step", "is_completed", "user")

class PasswordChange(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Avval login qiling")

        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": "Eski parol noto'g'ri"})

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Parollar mos emas"})

        validate_password(attrs["new_password"], user=user)
        return attrs

class ForgotPassword(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def validate(self, attrs):
        email = attrs.get("email")
        phone_number = attrs.get("phone_number")

        if not email and not phone_number:
            raise serializers.ValidationError("Email yoki phone number kiritish majburiy")
        if email and phone_number:
            raise serializers.ValidationError("Faqat bittasi yuborilishi kerak")

        user = User.objects.filter(
            Q(email=email) if email else Q(phone_number=phone_number)
        ).first()
        if not user:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")

        attrs["user"] = user
        return attrs

class ResetPassword(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    code = serializers.CharField(max_length=6)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        phone_number = attrs.get("phone_number")

        if not email and not phone_number:
            raise serializers.ValidationError("Email yoki phone number kiritish majburiy")
        if email and phone_number:
            raise serializers.ValidationError("Faqat bittasi yuborilishi kerak")

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Parollar mos emas"})

        user = User.objects.filter(
            Q(email=email) if email else Q(phone_number=phone_number)
        ).first()
        if not user:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")

        otp = OTPCode.objects.filter(
            purpose=Purpose.RESET_PASSWORD,
            is_used=False,
            email=email if email else None,
            phone_number=phone_number if phone_number else None,
        ).order_by("-created_at").first()
        if not otp or otp.is_expired() or otp.code != attrs["code"]:
            raise serializers.ValidationError({"code": "Kod noto'g'ri yoki eskirgan"})

        validate_password(attrs["password"], user=user)
        attrs["user"] = user
        attrs["otp"] = otp
        return attrs
