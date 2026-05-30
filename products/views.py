from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, ProductImage, Status
from products.serializers import ProductImageSerializer, ProductSerializer, ProductStatusSerializer


class ProductListCreateView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.select_related("category", "seller").prefetch_related("images")
        user = self.request.user

        if self.request.query_params.get("mine") == "true" and user.is_authenticated:
            queryset = queryset.filter(seller=user)
        else:
            queryset = queryset.filter(status=Status.PUBLISHED)

        category = self.request.query_params.get("category")
        search = self.request.query_params.get("search")
        if category:
            queryset = queryset.filter(Q(category_id=category) | Q(category__slug=category))
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Product.objects.select_related("category", "seller").prefetch_related("images")
        user = self.request.user
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return queryset.filter(seller=user)
        if user.is_authenticated:
            return queryset.filter(Q(status=Status.PUBLISHED) | Q(seller=user))
        return queryset.filter(status=Status.PUBLISHED)


class ProductImageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        product = Product.objects.filter(slug=slug, seller=request.user).first()
        if not product:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductImageSerializer(data={**request.data, "product": product.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductImageDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        image = ProductImage.objects.select_related("product").filter(id=pk, product__seller=request.user).first()
        if not image:
            return Response({"detail": "Rasm topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, slug):
        product = Product.objects.filter(slug=slug, seller=request.user).first()
        if not product:
            return Response({"detail": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product.status = serializer.validated_data["status"]
        product.save(update_fields=["status", "updated_at"])
        return Response(ProductSerializer(product, context={"request": request}).data)
