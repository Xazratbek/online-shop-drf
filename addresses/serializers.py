from rest_framework import serializers
from addresses.models import UserAddress

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"
