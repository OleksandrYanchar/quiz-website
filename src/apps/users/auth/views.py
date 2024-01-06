from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView    
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from users.models import User
from .serializers import ChangePasswordSerializer, UserAuthSerializer
from .tokens import EmailVerificationTokenGenerator, create_jwt_pair_for_user
from rest_framework.generics import UpdateAPIView   
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated   

class UserRegistrationView(APIView):
    def post(self, request: Request):
        serializer = UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get("password"))
            user.save()
            self._send_email_verification(user)
            return Response(
                data={
                    "user_id": str(user.id),
                    "tokens": create_jwt_pair_for_user(user=user),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _send_email_verification(self, user: User):
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        body = render_to_string(
            'email_verification.html',
            {
                "user": user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': EmailVerificationTokenGenerator().make_token(user),
            }
        )
        user.email_user(subject=subject, message=body)


class ActivateView(APIView):
    def get(self, request, uidb64, token):
        unique_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=unique_id)

        if user and EmailVerificationTokenGenerator().check_token(user, token):
            user.is_activeted = True
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
            return Response(data={"message": "Invalid username or password"})

class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token 
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'token': token.key}, status=status.HTTP_200_OK)
