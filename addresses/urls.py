from django.urls import path

from addresses.views import AddressDetailView, AddressListCreateView

urlpatterns = [
    path("", AddressListCreateView.as_view()),
    path("<uuid:pk>/", AddressDetailView.as_view()),
]
