from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from user import serializers
from rest_framework.authtoken.models import Token
from user.serializers import LoginSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomAuthToken(APIView):
    @swagger_auto_schema(
        operation_description="Log in with email and password to obtain authentication token",
        request_body=LoginSerializer,
        responses={200: openapi.Response("Login successful", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication token'),
            }
        ))}
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
