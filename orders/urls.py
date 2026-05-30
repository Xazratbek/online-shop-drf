from django.urls import path

from orders.views import CancelOrderView, CreateOrderView, OrderDetailView, OrderListView

urlpatterns = [
    path("", OrderListView.as_view()),
    path("create/", CreateOrderView.as_view()),
    path("<uuid:pk>/", OrderDetailView.as_view()),
    path("<uuid:pk>/cancel/", CancelOrderView.as_view()),
]
