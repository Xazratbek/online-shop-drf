from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, Status
from wishlist.models import Wishlist, WishlistItem
from wishlist.serializers import WishlistAddSerializer, WishlistSerializer


class WishlistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_wishlist(self, user):
        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        return Wishlist.objects.prefetch_related("items__product__images", "items__product__category").get(id=wishlist.id)

    def get(self, request):
        wishlist = self.get_wishlist(request.user)
        return Response(WishlistSerializer(wishlist, context={"request": request}).data)


class WishlistAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WishlistAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.filter(id=serializer.validated_data["product"], status=Status.PUBLISHED).first()
        if not product:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        wishlist = Wishlist.objects.prefetch_related("items__product__images", "items__product__category").get(id=wishlist.id)
        return Response(WishlistSerializer(wishlist, context={"request": request}).data, status=status.HTTP_201_CREATED)


class WishlistItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = WishlistItem.objects.filter(id=pk, wishlist__user=request.user).first()
        if not item:
            return Response({"detail": "Wishlist elementi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
