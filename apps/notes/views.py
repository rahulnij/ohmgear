from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import Notes
from serializer import NotesSerializer
# Create your views here.
class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
