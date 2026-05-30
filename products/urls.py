from django.urls import path

from products.views import (
    ProductDetailView,
    ProductImageCreateView,
    ProductImageDeleteView,
    ProductListCreateView,
    ProductStatusView,
)

urlpatterns = [
    path("", ProductListCreateView.as_view()),
    path("<slug:slug>/", ProductDetailView.as_view()),
    path("<slug:slug>/images/", ProductImageCreateView.as_view()),
    path("<slug:slug>/status/", ProductStatusView.as_view()),
    path("images/<uuid:pk>/", ProductImageDeleteView.as_view()),
]
