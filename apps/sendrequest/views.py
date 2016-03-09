#------------ Third Party Imports ----------#
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
import boto3
#------------ Third Party Imports ----------#
#------------------ Local app imports ------#
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
#---------------------------End-------------#
# Create your views here.

class SendNotification(viewsets.ModelViewSet):

    queryset  = None.objects.all()
    serializer_class = None
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def list(self,request):
        return CustomeResponse({'msg':"GET METHOD NOT ALLOWD"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  
    def create(self,request,call_from_function=None,offline_data=None):
        return CustomeResponse({'msg':"POST METHOD NOT ALLOWD"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   
    def destroy(self, request, pk=None):
        return CustomeResponse({'msg':"DELETE METHOD NOT ALLOWD"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  
    
    
    @list_route(methods=['post'],)
    def invite_to_businesscard(self, request):
        client = boto3.client('sns')
        response = client.list_topics()
                           
        return CustomeResponse(response,status=status.HTTP_200_OK)