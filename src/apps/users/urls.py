from django.urls import path

from . import views
from users.auth.views import ActivateView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all/', views.UserListView.as_view()),
    path('<str:pk>/',views.UserView.as_view()),
    path('profile/email-verification/<str:uidb64>/<str:token>/', ActivateView.as_view(), name='email-verification'),

]