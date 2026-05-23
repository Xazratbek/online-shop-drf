from django.db import models
from common.models import BaseModel

class Gender(models.TextChoices):
    MALE = "male", "Erkak"
    FEMALE = "female", "Ayol"

class ProfileRole(models.TextChoices):
    BUYER = "buyer", "Sotib oluvchi"
    SELLER = "seller", "Sotuvchi"

class Profile(BaseModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(
        max_length=10,
        choices=ProfileRole.choices,
        default=ProfileRole.BUYER
    )
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True
    )
    preferred_language = models.CharField(max_length=20, default="uz")
    shop_name = models.CharField(max_length=255, blank=True)
    seller_description = models.TextField(blank=True)
    is_verified_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
