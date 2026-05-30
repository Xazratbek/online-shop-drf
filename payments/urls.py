from django.urls import path

from payments.views import MarkPaymentPaidView, PaymentDetailView, PaymentListCreateView

urlpatterns = [
    path("", PaymentListCreateView.as_view()),
    path("<uuid:pk>/", PaymentDetailView.as_view()),
    path("<uuid:pk>/paid/", MarkPaymentPaidView.as_view()),
]
