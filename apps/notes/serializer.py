from django.conf.urls import url, include
from apps.notes.models import Notes
from rest_framework import routers, serializers, viewsets


class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
