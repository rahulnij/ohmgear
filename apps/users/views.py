from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from apps.users.models import User
from apps.users.models import Profile
from serializer import UserSerializer
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