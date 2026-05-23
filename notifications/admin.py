from django.contrib import admin

from notifications.models import Notification, NotificationPreference


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "notification_type", "is_read", "created_at")
    search_fields = ("title", "message", "user__username", "user__email")
    list_filter = ("notification_type", "is_read")
    ordering = ("-created_at",)


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "order_updates", "payment_updates", "promotions", "system_updates")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)
