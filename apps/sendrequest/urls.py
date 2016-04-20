from . import views as sendrequest_view

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/send_accept_request', sendrequest_view.SendAcceptRequest)
#router.register(r'api/sendrequest', sendrequest_view.SendAcceptRequest)
router.register(r'api/greyrequest', sendrequest_view.GreyInvitationViewSet)
urlpatterns = router.urls
