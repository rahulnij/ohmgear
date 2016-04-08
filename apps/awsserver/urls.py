from rest_framework.routers import DefaultRouter

from .views import AwsActivity


router = DefaultRouter()
router.register(r'api/aws', AwsActivity)
urlpatterns = router.urls
