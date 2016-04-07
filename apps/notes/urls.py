from . import views as notes_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/notes', notes_views.NotesViewSet)
urlpatterns = router.urls