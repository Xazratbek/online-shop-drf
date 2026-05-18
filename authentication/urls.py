from django.urls import path

from authentication.views import (
    CompleteProfileView,
    LoginView,
    ProfileView,
    RegistrationSessionDetailView,
    StartSignupView,
    UploadAvatarView,
    VerifySignupOTPView,
)

urlpatterns = [
    path("signup/start/", StartSignupView.as_view()),
    path("signup/verify/", VerifySignupOTPView.as_view()),
    path("signup/profile/", CompleteProfileView.as_view()),
    path("signup/avatar/", UploadAvatarView.as_view()),
    path("signup/session/<uuid:session_id>/", RegistrationSessionDetailView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", ProfileView.as_view()),
]
