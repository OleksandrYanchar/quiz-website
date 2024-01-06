from django.urls import include, path

from . import views
from users.auth.views import ActivateView, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('all/', views.UserListView.as_view(), name="users"),
    path('', include('users.auth.urls')),

    path('<str:pk>/',views.UserView.as_view(), name="profile"),

]