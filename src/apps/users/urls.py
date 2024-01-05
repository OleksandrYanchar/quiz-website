from django.urls import path

from . import views




urlpatterns = [
    path('all/', views.UserListView.as_view()),
    path('<str:pk>/',views.UserView.as_view()),
    
]
