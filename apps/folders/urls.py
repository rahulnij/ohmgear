from . import views as folder_view

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/folder',folder_view.FolderViewSet)
urlpatterns = router.urls