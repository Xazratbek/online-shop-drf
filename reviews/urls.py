from django.urls import path

from reviews.views import ReviewDetailView, ReviewListCreateView

urlpatterns = [
    path("", ReviewListCreateView.as_view()),
    path("<uuid:pk>/", ReviewDetailView.as_view()),
]
