# --------- Import Python Modules ----------- #
# ------------ Third Party Imports ---------- #
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import rest_framework.status as status
# ----------------- Local app imports ------ #
from ohmgear.token_authentication import ExpiringTokenAuthentication
from apps.sendrequest.serializer import SendRequestSerializer
from models import SendRequest
from ohmgear.functions import CustomeResponse
# ---------------------------End------------- #


class RequestListViewSet(viewsets.ModelViewSet):

    queryset = SendRequest.objects.all()
    serializer_class = SendRequestSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):

        user_id = request.user
        sent_request = request.query_params.get('sent_request', None)
        received_request = request.query_params.get('received_request', None)
        # get the list of request which user sent to other business card
        if sent_request:
            queryset = self.queryset.select_related('sender_business_card_id').filter(sender_user_id=user_id)            
            serializer = self.serializer_class(
                queryset, many=True, context={'filter_type': 'sent'})
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)

        # get the list of request which user receive
        if received_request:
            queryset = self.queryset.filter(receiver_user_id=user_id)
            serializer = self.serializer_class(
                queryset, many=True, context={'filter_type': 'received'})
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)

        return CustomeResponse(
            {
                'msg': "Please provide sent_request or received_request parameter"},
            status=status.HTTP_400_BAD_REQUEST,
            validate_errors=1)

        return CustomeResponse({'msg': "GET METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def create(self, request, call_from_function=None, offline_data=None):
        return CustomeResponse({'msg': "POST METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def destroy(self, request, pk=None):
        return CustomeResponse({'msg': "DELETE METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
