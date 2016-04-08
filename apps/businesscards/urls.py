from django.conf.urls import url, include
from . import views as businesscards_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/businesscard', businesscards_views.BusinessViewSet)
router.register(r'api/businesscardidentifier',
                businesscards_views.BusinessCardIdentifierViewSet)
router.register(r'api/businesscardaddskill',
                businesscards_views.BusinessCardAddSkillViewSet)
router.register(r'api/businesscardskillavailable',
                businesscards_views.BusinessCardSkillAvailableViewSet)
router.register(r'api/businesscardshistory',
                businesscards_views.BusinessCardHistoryViewSet)
urlpatterns = router.urls
urlpatterns += [url(r'^api/businesscardsummary/$',
                    businesscards_views.CardSummary.as_view()), ]
