from . import views as sendrequest_view
from view_request_list_api import RequestListViewSet as request_list 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/send_accept_request', sendrequest_view.SendAcceptRequest)
router.register(r'api/request_list', request_list)
#router.register(r'api/sendrequest', sendrequest_view.SendAcceptRequest)
router.register(r'api/greyrequest', sendrequest_view.GreyInvitationViewSet)
urlpatterns = router.urls
