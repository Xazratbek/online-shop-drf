from django.urls import path

from categories.views import CategoryDetailView, CategoryListCreateView

urlpatterns = [
    path("", CategoryListCreateView.as_view()),
    path("<slug:slug>/", CategoryDetailView.as_view()),
]
