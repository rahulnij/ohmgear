from django.conf.urls import url, include
from apps.identifiers.models import Identifier
from rest_framework import routers, serializers, viewsets
       
class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
            