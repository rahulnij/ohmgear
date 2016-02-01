#------------ Import Python Modules -----------#

#-------------------------------------------#

#------------ Third Party Imports ----------#
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
import rest_framework.status as status
#-------------------------------------------#

#------------ Local app imports ------#
from apps.businesscards.views import BusinessViewSet
from apps.businesscards.models import BusinessCard
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
#-------------------------------------------#

# Create your views here.
#---------------------------- Update data on server ----------------------------#
class OfflineSendReceiveDataViewSet(viewsets.ModelViewSet):
    
      queryset = BusinessCard.objects.none()
      serializer_class = None
      authentication_classes = (ExpiringTokenAuthentication,)
      permission_classes = (IsAuthenticated,)
      
      
      def create(self, request): 
          return CustomeResponse({'msg':"NOT ALLOWED"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
      
      @list_route(methods=['post'],)
      def send(self, request):
          # data format {"businesscard": [{"operation": "add","json_data": [{}, {}]}, {	"operation": "update","json_data": [{}, {}]}] }
          
          try:           
           user_id = request.user.id
          except:
           user_id = None
           
          try:
             businesscard = request.data['businesscard']
          except:
             businesscard = ''
          
          final_return_data = {}
          if businesscard:
              business_card_class = BusinessViewSet() 
              for raw_data in businesscard:
                  if raw_data["operation"] == 'add':
                     #-----------------  Create the business card ---------------------------# 
                    business_data = []
                    if raw_data["json_data"]:
                      #------------- execute all business card-----------------------#  
                      for items in raw_data["json_data"]:  
                        data = {}
                        data['user_id'] = user_id
                        data['bcard_json_data'] = raw_data['bcard_json_data']
                        business_card_response = business_card_class.create(request,1,data)
                        if business_card_response["status"]:
                           return CustomeResponse(business_card_response["data"],status=status.HTTP_201_CREATED)
                        else:
                           return CustomeResponse(business_card_response["data"],status=status.HTTP_400_BAD_REQUEST, validate_errors=1) 
                    
                     #------------------- End -----------------------------------------------#
                  if raw_data["operation"] == 'edit':
                     #-----------------  Edit the business card ---------------------------#
                     pass
                     #------------------- End -----------------------------------------------#    
              return CustomeResponse({'msg':"NOT ALLOWED"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)     
      @list_route(methods=['get'],)
      def receive(self, request):
          pass      

#---------------------------- End ----------------------------------------------#

#---------------------------  Fetch data from server ---------------------------#


#---------------------------  End ----------------------------------------------#
