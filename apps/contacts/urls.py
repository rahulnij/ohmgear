from . import views as contacts_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/contactmedia', contacts_views.ContactMediaViewSet)
router.register(r'api/contacts',contacts_views.storeContactsViewSet)
urlpatterns = router.urls