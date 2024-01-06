from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import MyTokenObtainPairView

from . import views

urlpatterns = [
    path("sign-up/", views.UserRegistrationView.as_view(), name="sig-nup"),
    path("log-in/", views.UserLoginView.as_view(), name="log-in"), 
    path("jwt/create/", MyTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token-verify"),
]