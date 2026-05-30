from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewListCreateView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.select_related("user", "product")
        product = self.request.query_params.get("product")
        if product:
            queryset = queryset.filter(Q(product_id=product) | Q(product__slug=product))
        if self.request.user.is_authenticated and self.request.query_params.get("mine") == "true":
            queryset = queryset.filter(user=self.request.user)
        else:
            queryset = queryset.filter(is_approved=True)
        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
