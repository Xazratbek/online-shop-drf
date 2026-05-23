from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "user", "method", "status", "amount", "currency", "paid_at")
    search_fields = ("order__id", "user__username", "user__email", "transaction_id", "provider")
    list_filter = ("method", "status", "currency")
    ordering = ("-created_at",)
