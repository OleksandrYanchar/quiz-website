from .models import User
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer, UserSerializer, UserListSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


class UserView(APIView):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    