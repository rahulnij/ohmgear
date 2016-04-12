
from . import views as identifiers_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/identifiers', identifiers_views.IdentifierViewSet)
urlpatterns = router.urls