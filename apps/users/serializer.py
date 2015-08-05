from django.conf.urls import url, include
from apps.users.models import User
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        read_only_fields = ('id','password') 