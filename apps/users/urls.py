from django.conf.urls import url, include

from . import views as users_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users/emails', users_views.UserEmailViewSet)
router.register(r'api/users', users_views.UserViewSet)
router.register(r'api/profile', users_views.ProfileViewSet)
router.register(r'api/sociallogin', users_views.SocialLoginViewSet)
router.register(r'api/sociallogin', users_views.SocialLoginViewSet)
urlpatterns = router.urls

urlpatterns += [url(r'^api/useractivity/$',
                    users_views.useractivity,
                    name='useractivity'),
                url(r'^api/account_confirmation/(?P<activation_key>\w+)/$',
                    users_views.useractivity,
                    name='registration_confirm'),
                url(r'^api/forgot_password/(?P<reset_password_key>\w+)/$',
                    users_views.useractivity,
                    name='forgot_password'),
                ]

from signals import *
