from rest_framework.routers import DefaultRouter

from . import views as staticpages_view


router = DefaultRouter()
router.register(r'api/staticpages', staticpages_view.StaticPagesViewSet)
urlpatterns = router.urls
