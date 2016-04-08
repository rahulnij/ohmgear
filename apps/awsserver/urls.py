from . import views as AWSActivity

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/aws',AWSActivity.AWSActivity)
urlpatterns = router.urls