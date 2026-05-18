from django.db import models
from common.models import BaseModel


class Cart(BaseModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE
    )

class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)