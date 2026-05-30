from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import AddCartItemSerializer, CartSerializer, UpdateCartItemSerializer


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return Cart.objects.prefetch_related("items__product__images", "items__product__category").get(id=cart.id)

    def get(self, request):
        cart = self.get_cart(request.user)
        return Response(CartSerializer(cart, context={"request": request}).data)


class AddCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
        if not created:
            new_quantity = item.quantity + quantity
            if product.stock < new_quantity:
                return Response({"quantity": "Omborda yetarli mahsulot yo'q"}, status=status.HTTP_400_BAD_REQUEST)
            item.quantity = new_quantity
            item.save(update_fields=["quantity", "updated_at"])
        cart = Cart.objects.prefetch_related("items__product__images", "items__product__category").get(id=cart.id)
        return Response(CartSerializer(cart, context={"request": request}).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        item = CartItem.objects.select_related("product", "cart").filter(id=pk, cart__user=request.user).first()
        if not item:
            return Response({"detail": "Savatcha elementi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]
        if item.product.stock < quantity:
            return Response({"quantity": "Omborda yetarli mahsulot yo'q"}, status=status.HTTP_400_BAD_REQUEST)
        item.quantity = quantity
        item.save(update_fields=["quantity", "updated_at"])
        return Response(CartSerializer(item.cart, context={"request": request}).data)

    def delete(self, request, pk):
        item = CartItem.objects.filter(id=pk, cart__user=request.user).first()
        if not item:
            return Response({"detail": "Savatcha elementi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClearCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
