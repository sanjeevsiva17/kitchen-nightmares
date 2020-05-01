from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


# Create your views here.


class SignUp(generics.CreateAPIView):
    """
    View for creating new user in the system
    """
    serializer_class = UserSerializer


class Login(ObtainAuthToken):
    """
    View for authenticating a user
    Creates auth token
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
