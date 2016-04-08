# Third Party Imports
from django.conf.urls import url, include
import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'user/location', views.UserLocationViewSet)
urlpatterns = router.urls
