from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets
from views import BusinessViewSet
router = routers.DefaultRouter()
router.register(r'businesscard', BusinessViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
