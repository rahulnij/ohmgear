from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import User,Profile,SocialLogin
from serializer import UserSerializer,ProfileSerializer,SocialLoginSerializer
from ohmgear.authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    authentication_classes = (ExpiringTokenAuthentication,)
#    permission_classes = (IsAuthenticated,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    
class SocialLoginViewSet(viewsets.ModelViewSet):
    queryset = SocialLogin.objects.all()
    serializer_class = SocialLoginSerializer