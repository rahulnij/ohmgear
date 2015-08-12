from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets
from views import UserViewSet,ProfileViewSet,SocialLoginViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'sociallogin',SocialLoginViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
