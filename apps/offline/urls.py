from . import views as offline_view

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/offline',offline_view.OfflineSendReceiveDataViewSet)
urlpatterns = router.urls