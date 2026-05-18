from django.urls import path

from .views import LoginView, SignupView, auth_page

app_name = "authentication"

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("auth-page/", auth_page, name="auth_page"),
]
