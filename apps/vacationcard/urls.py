from django.conf.urls import url, include

from . import views as vacationcard_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/vacationcard',vacationcard_views.VacationCardViewSet)
router.register(r'api/businesscardvacation',vacationcard_views.BusinessCardVacationViewSet)
urlpatterns = router.urls

urlpatterns += [
	url(r'^vacationcard/merge$', vacationcard_views.VacationCardMerge.as_view(), name='vacationcard_merge')
]