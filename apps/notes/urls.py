from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets
from views import NotesViewSet
router = routers.DefaultRouter()
router.register(r'notes', NotesViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
]

from signals import *
