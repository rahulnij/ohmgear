from . import views as cron_view

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/cron/update_contact_link_status',cron_view.UpdateContactLinkStatusCron)
urlpatterns = router.urls