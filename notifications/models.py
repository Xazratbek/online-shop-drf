from django.db import models

from common.models import BaseModel


class NotificationType(models.TextChoices):
    SYSTEM = "system", "System"
    ORDER = "order", "Order"
    PAYMENT = "payment", "Payment"
    PROMOTION = "promotion", "Promotion"


class Notification(BaseModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title


class NotificationPreference(BaseModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="notification_preference"
    )
    order_updates = models.BooleanField(default=True)
    payment_updates = models.BooleanField(default=True)
    promotions = models.BooleanField(default=True)
    system_updates = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
