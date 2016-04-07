from django.conf.urls import url, include
from models import StaticPages
from rest_framework import routers, serializers, viewsets


class StaticPagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaticPages
