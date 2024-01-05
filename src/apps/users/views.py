from .models import User
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import UserSerializer, UserListSerializer
from rest_framework.response import Response
from rest_framework import status

class UserView(APIView):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer