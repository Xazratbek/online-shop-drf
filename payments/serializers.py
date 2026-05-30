from rest_framework import serializers

from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "order",
            "user",
            "method",
            "status",
            "amount",
            "currency",
            "transaction_id",
            "provider",
            "paid_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "status", "amount", "paid_at", "created_at", "updated_at")
