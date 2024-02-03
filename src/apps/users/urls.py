from django.urls import include, path

from . import views
from users.auth.views import ActivateView, ChangePasswordView


urlpatterns = [
    path('all/', views.UserListView.as_view(), name="users"),
    path('', include('users.auth.urls')),

    path('profile/<str:pk>/',views.UserView.as_view(), name="profile"),

]