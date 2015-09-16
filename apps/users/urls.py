from django.conf.urls import include, url
from rest_framework import routers, serializers, viewsets
from views import UserViewSet,ProfileViewSet,SocialLoginViewSet,useractivity
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'sociallogin',SocialLoginViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^useractivity/$','apps.users.views.useractivity',name='useractivity'),
    url(r'^account_confirmation/(?P<activation_key>\w+)/$','apps.users.views.useractivity',name='registration_confirm'),
    url(r'^forgot_password/(?P<reset_password_key>\w+)/$','apps.users.views.useractivity',name='forgot_password'),
]

from signals import *