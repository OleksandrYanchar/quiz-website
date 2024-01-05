from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'bio', 'picture','slug','date_added','date_changed']
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'slug']