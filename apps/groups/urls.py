from . import views as groups_view

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/group', groups_view.GroupViewSet)
router.register(r'api/groupcontacts', groups_view.GroupContactsViewSet)
urlpatterns = router.urls
