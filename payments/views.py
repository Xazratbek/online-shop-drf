from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Status as OrderStatus
from payments.models import Payment, PaymentStatus
from payments.serializers import PaymentSerializer


class PaymentListCreateView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related("order").order_by("-created_at")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data["order"]
        if order.user != request.user:
            return Response({"order": "Bu buyurtma sizga tegishli emas"}, status=status.HTTP_400_BAD_REQUEST)
        if order.status == OrderStatus.CANCELLED:
            return Response({"order": "Bekor qilingan buyurtmaga to'lov qilib bo'lmaydi"}, status=status.HTTP_400_BAD_REQUEST)
        payment = serializer.save(user=request.user, amount=order.total_price)
        return Response(PaymentSerializer(payment, context={"request": request}).data, status=status.HTTP_201_CREATED)


class PaymentDetailView(RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related("order")


class MarkPaymentPaidView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        payment = Payment.objects.select_related("order").filter(id=pk, user=request.user).first()
        if not payment:
            return Response({"detail": "To'lov topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        payment.status = PaymentStatus.PAID
        payment.paid_at = timezone.now()
        payment.save(update_fields=["status", "paid_at", "updated_at"])
        if payment.order.status == OrderStatus.PENDING:
            payment.order.status = OrderStatus.PAID
            payment.order.save(update_fields=["status", "updated_at"])
        return Response(PaymentSerializer(payment, context={"request": request}).data)
