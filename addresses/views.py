from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from addresses.models import UserAddress
from addresses.serializers import UserAddressSerializer


class AddressListCreateView(ListCreateAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user).order_by("-is_default", "-created_at")

    def perform_create(self, serializer):
        address = serializer.save(user=self.request.user)
        if address.is_default:
            UserAddress.objects.filter(user=self.request.user).exclude(id=address.id).update(is_default=False)


class AddressDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        address = serializer.save()
        if address.is_default:
            UserAddress.objects.filter(user=self.request.user).exclude(id=address.id).update(is_default=False)
