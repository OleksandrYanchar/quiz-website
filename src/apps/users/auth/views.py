from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView    
from django.utils.encoding import  force_str
from .services import _send_email
from users.models import User
from .serializers import ChangePasswordSerializer, ResetUserPasswordSerializer, UserAuthSerializer, CheckResetUserPasswordEmailSerializer
from .tokens import EmailTokenGenerator, create_jwt_pair_for_user
from rest_framework.generics import UpdateAPIView   
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated   
from django.utils.http import  urlsafe_base64_decode

class UserRegistrationView(APIView):
    def post(self, request: Request):
        serializer = UserAuthSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get("password"))
            template = 'email_verification.html'
            subject ="Activate email"
            _send_email(request, user, template, subject)  
            user.save()

            return Response(
                data={
                    "user_id": str(user.id),
                    "tokens": create_jwt_pair_for_user(user=user),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class ActivateView(APIView):
    def get(self, request, uidb64, token):
        try:
            unique_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=unique_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"message": "Invalid activation link", "status": status.HTTP_400_BAD_REQUEST})

        if user and EmailTokenGenerator().check_token(user, token):
            user.is_activated = True
            user.save()
            return Response({"message": "Account activated", "status": status.HTTP_200_OK})

        return Response({"message": "Account activation failed", "status": status.HTTP_400_BAD_REQUEST})
    
class UserLoginView(APIView):
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response(
                data={
                    "user_id": str(user.id),
                    "tokens": create_jwt_pair_for_user(user=user),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(data={"message": "Invalid username or password", "status": status.HTTP_400_BAD_REQUEST})

class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({'message':"password changed" }, status=status.HTTP_200_OK)
    
class CheckResetUserPasswordEmailView(UpdateAPIView):
    serializer_class = CheckResetUserPasswordEmailSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            if email:
                user = get_object_or_404(User, email=email)
                _send_email(request, user, 'password-reset.html', 'Reset Your Password')
                return Response({'message': 'Reset password email sent successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPasswordView(UpdateAPIView):
    serializer_class = ResetUserPasswordSerializer

    def get_user(self, uidb64):
        try:
            unique_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=unique_id)
            return user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def update(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user and EmailTokenGenerator().check_token(user, token):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save(user=user)

            return Response({'message': "Password was reset"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Error", "status": status.HTTP_400_BAD_REQUEST})
