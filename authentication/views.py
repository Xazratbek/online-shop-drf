from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import AuthType, User
from authentication.models import OTPCode, Purpose, RegistrationSession, Step
from authentication.serializers import (
    CompleteProfileSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegistrationSessionSerializer,
    StartRegistrationSerializer,
    UploadAvatarSerializer,
    VerifyOTPSerializer,
)
from authentication.utils import generate_otp, generate_password, generate_username


class StartSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StartRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        phone_number = serializer.validated_data.get("phone_number")
        otp = generate_otp()

        with transaction.atomic():
            user = User.objects.create_user(
                username=generate_username(),
                password=generate_password(),
                email=email,
                phone_number=phone_number,
                auth_type=AuthType.EMAIL if email else AuthType.PHONE,
            )
            session = RegistrationSession.objects.create(user=user, current_step=Step.VERIFY)
            OTPCode.objects.create(
                email=email,
                phone_number=phone_number,
                code=otp,
                purpose=Purpose.REGISTER,
                expires_at=OTPCode.get_expiry(),
            )

        if email:
            send_mail("Tasdiqlash kodi", f"Sizning kod: {otp}", None, [email], fail_silently=True)
        else:
            print(f"[PHONE OTP] {phone_number}: {otp}")

        return Response({"session_id": str(session.id), "step": Step.VERIFY}, status=status.HTTP_201_CREATED)


class VerifySignupOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = RegistrationSession.objects.select_related("user").filter(id=serializer.validated_data["session_id"]).first()
        if not session:
            return Response({"detail": "Session topilmadi"}, status=404)

        user = session.user
        otp = OTPCode.objects.filter(
            purpose=Purpose.REGISTER,
            is_used=False,
            email=user.email if user.email else None,
            phone_number=user.phone_number if user.phone_number else None,
        ).order_by("-created_at").first()

        if not otp or otp.is_expired() or otp.code != serializer.validated_data["code"]:
            return Response({"detail": "Kod noto'g'ri yoki eskirgan"}, status=400)

        otp.is_used = True
        otp.save(update_fields=["is_used"])

        if user.email:
            user.is_email_verified = True
        if user.phone_number:
            user.is_phone_verified = True
        user.save(update_fields=["is_email_verified", "is_phone_verified", "updated_at"])

        session.current_step = Step.PROFILE
        session.save(update_fields=["current_step", "updated_at"])

        return Response({"step": Step.PROFILE})


class CompleteProfileView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CompleteProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = RegistrationSession.objects.select_related("user").filter(id=serializer.validated_data["session_id"]).first()
        if not session:
            return Response({"detail": "Session topilmadi"}, status=404)

        user = session.user
        user.first_name = serializer.validated_data["full_name"]
        user.username = serializer.validated_data["username"]
        user.bio = serializer.validated_data.get("bio", "")
        user.set_password(serializer.validated_data["password"])
        user.save()

        session.current_step = Step.AVATAR
        session.save(update_fields=["current_step", "updated_at"])

        return Response({"step": Step.AVATAR})


class UploadAvatarView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UploadAvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session = RegistrationSession.objects.select_related("user").filter(id=serializer.validated_data["session_id"]).first()
        if not session:
            return Response({"detail": "Session topilmadi"}, status=404)

        avatar = serializer.validated_data.get("avatar")
        if avatar:
            session.user.avatar = avatar
            session.user.save(update_fields=["avatar", "updated_at"])

        session.current_step = Step.COMPLETED
        session.is_completed = True
        session.save(update_fields=["current_step", "is_completed", "updated_at"])

        return Response({"step": Step.COMPLETED, "profile": ProfileSerializer(session.user).data})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": ProfileSerializer(user).data,
        })


class ProfileView(APIView):
    def get(self, request):
        return Response(ProfileSerializer(request.user).data)


class RegistrationSessionDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, session_id):
        session = RegistrationSession.objects.select_related("user").filter(id=session_id).first()
        if not session:
            return Response({"detail": "Session topilmadi"}, status=404)
        return Response(RegistrationSessionSerializer(session).data)


from django.views.generic import TemplateView

class AuthPageView(TemplateView):
    template_name = "authentication/auth.html"
