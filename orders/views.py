from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from orders.models import Order, OrderItem, Status
from orders.serializers import OrderSerializer


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product__images").order_by("-created_at")


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product__images")


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).prefetch_related("items__product").first()
        if not cart or not cart.items.exists():
            return Response({"detail": "Savatcha bo'sh"}, status=status.HTTP_400_BAD_REQUEST)

        items = list(cart.items.select_related("product"))
        for item in items:
            if item.product.stock < item.quantity:
                return Response(
                    {"detail": f"{item.product.title} omborda yetarli emas"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        total_price = sum((item.product.discount_price or item.product.price) * item.quantity for item in items)
        order = Order.objects.create(user=request.user, total_price=total_price)

        order_items = []
        for item in items:
            product = item.product
            price = product.discount_price or product.price
            order_items.append(OrderItem(order=order, product=product, quantity=item.quantity, price=price))
            product.stock -= item.quantity
            product.save(update_fields=["stock", "updated_at"])

        OrderItem.objects.bulk_create(order_items)
        cart.items.all().delete()
        order = Order.objects.prefetch_related("items__product__images").get(id=order.id)
        return Response(OrderSerializer(order, context={"request": request}).data, status=status.HTTP_201_CREATED)


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, pk):
        order = Order.objects.filter(id=pk, user=request.user).prefetch_related("items__product").first()
        if not order:
            return Response({"detail": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        if order.status != Status.PENDING:
            return Response({"detail": "Faqat pending buyurtmani bekor qilish mumkin"}, status=status.HTTP_400_BAD_REQUEST)

        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save(update_fields=["stock", "updated_at"])

        order.status = Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        return Response(OrderSerializer(order, context={"request": request}).data)
