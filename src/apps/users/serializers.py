from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'bio', 'picture','slug','date_added','date_changed', 'is_activeted']
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'slug']
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['username'] = user.username
        token['slug'] = user.slug



        return token