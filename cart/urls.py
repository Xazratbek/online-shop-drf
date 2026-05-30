from django.urls import path

from cart.views import AddCartItemView, CartDetailView, CartItemDetailView, ClearCartView

urlpatterns = [
    path("", CartDetailView.as_view()),
    path("add/", AddCartItemView.as_view()),
    path("clear/", ClearCartView.as_view()),
    path("items/<uuid:pk>/", CartItemDetailView.as_view()),
]
