from rest_framework.routers import DefaultRouter

from . import views as notes_views

router = DefaultRouter()
router.register(r'api/notes', notes_views.NotesViewSet)
urlpatterns = router.urls
