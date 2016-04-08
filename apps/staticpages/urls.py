from . import views as staticpages_view

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/staticpages',staticpages_view.StaticPagesViewSet)
urlpatterns = router.urls