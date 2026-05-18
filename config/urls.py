from django.contrib import admin
from django.urls import include, path
from authentication.views import AuthPageView

urlpatterns = [
    path('', AuthPageView.as_view()),
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
]
