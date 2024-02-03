from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import MyTokenObtainPairView

from . import views

urlpatterns = [
    path("sign-up/", views.UserRegistrationView.as_view(), name="sign-up"),
    path("log-in/", views.UserLoginView.as_view(), name="log-in"), 
    path('email-verification/<str:uidb64>/<str:token>/', views.ActivateView.as_view(), name='email-verification'),
    path('password-reset/', views.CheckResetUserPasswordEmailView.as_view(), name='reset-password'),
    path('password-reset-user/<str:uidb64>/<str:token>/', views.ResetPasswordView.as_view(),name='reset-user-password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('', include('social_django.urls',namespace = 'social')),
    path('auth/', views.auth, name ='auth'),
    
    path("jwt/create/", MyTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token-verify"),
]