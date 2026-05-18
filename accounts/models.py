from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import BaseModel

class AuthType(models.TextChoices):
    EMAIL = "email", "Email"
    PHONE = "phone", "Phone"

class User(AbstractUser,BaseModel):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    auth_type = models.CharField(
        max_length=10,
        choices=AuthType.choices
    )
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username