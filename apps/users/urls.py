from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets
from views import UserViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
