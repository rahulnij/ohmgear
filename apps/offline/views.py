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
from apps.usersetting.models import Setting,UserSetting
from apps.usersetting.serializer import UserSignupSettingSerializer
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


      @list_route(methods=["post"],)
      # update multiple settings in case of offline----------#
      def updatemultiplerecord(self,request):
        try:
            getkey  =request.DATA

            settingdata = Setting.objects.all()
            usersettingdata = UserSetting.objects.all()
            
            usersettingexist = UserSetting.objects.filter(user_id=request.user.id)
            if usersettingexist:
            
           # get corresponding key and setting id from setting table-----------#
                tempContainer = []
                count = 0
                for i in getkey: 
                    innerloop= 0
                    for j in settingdata:
                        data   = {}
                        if i==j.key:
                            data = {"key":j.key,"setting_id":j.id}
                            datas = tempContainer.append(data)                        
                            count=count+1
            
            # make dictionary for setting_id corresponding to key and its value to be update in usersetting table-------#
            
                newtempContainer = []
                counter=0
                for getdata in getkey:
                    existingdata    =   0   
                    for i in tempContainer:
                        data    =   {}
                        if getdata in i['key']:
                            value   =  getkey[i['key']]
                            data    =   {"setting_id":i['setting_id'],"value":value,"user_id":request.user.id}
                            datas = newtempContainer.append(data)                        
                            counter=counter+1

            # update usersetting records corresponding to setting_id in usersetting table--------#
                    j=0         
                    for i in usersettingdata:
                        for k in newtempContainer :
                            if i.setting_id.id == k['setting_id'] and k['user_id']==i.user_id.id:
                                UserSetting.objects.filter(user_id=request.user.id,setting_id=k['setting_id']).update(value=k['value'])
                                j=j+1
                                
                if newtempContainer:
                    return CustomeResponse({"msg":"Data has been updated"},status=status.HTTP_200_OK)
                else:
                    return CustomeResponse({"msg":" No Data found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                        
            else:
                return CustomeResponse({"msg":" No Data found for this user"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                                                                                     
        except:
            return CustomeResponse({"msg":"Data not found"},validate_errors=1)
          



#---------------------------- End ----------------------------------------------#

#---------------------------  Fetch data from server ---------------------------#


#---------------------------  End ----------------------------------------------#
