from . import views as setting_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/usersetting',setting_views.UserSettingViewSet)
router.register(r'api/languagesetting',setting_views.LanguageSettingViewSet)
router.register(r'api/displaycontactsetting',setting_views.DisplayContactNameAsViewSet)
router.register(r'api/businesscardshistory', businesscards_views.BusinessCardHistoryViewSet)
urlpatterns = router.urls