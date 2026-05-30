from django.urls import path

from wishlist.views import WishlistAddView, WishlistDetailView, WishlistItemDeleteView

urlpatterns = [
    path("", WishlistDetailView.as_view()),
    path("add/", WishlistAddView.as_view()),
    path("items/<uuid:pk>/", WishlistItemDeleteView.as_view()),
]
