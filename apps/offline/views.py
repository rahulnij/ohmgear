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
from apps.vacationcard.views  import VacationCardViewSet
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
             businesscard_copy = request.data.copy()
          except:
             businesscard = ''
          
          final_return_data = {}
          if businesscard:
              business_card_class = BusinessViewSet() 
              position = 0
              for raw_data in businesscard:
                  
                  #-----------------  Create the business card ---------------------------#
                  if raw_data["operation"] == 'add': 
                    business_data = []
                    if raw_data["json_data"]:
                      #------------- execute all business card-----------------------#  
                      for items in raw_data["json_data"]:  
                            data = {}
                            data['user_id'] = user_id
                            try:
                              data['bcard_json_data'] = items['bcard_json_data']
                            except:
                              data['bcard_json_data'] =''
                            
                            #------------- Local business card id --------------#
                            try:
                              local_business_id = items['local_business_id']
                            except:
                              local_business_id =''  
                            #-------------------- End --------------------------#
                            
                            business_card_response = business_card_class.create(request,1,data)
                            if business_card_response["status"]:
                               try:
                                 bcard_id = business_card_response["data"]["id"]
                               except:
                                 bcard_id = business_card_response["data"]  
                               business_data.append({"local_business_id":local_business_id,"bcard_id":bcard_id})
                            else:
                               business_data.append({"local_business_id":local_business_id,"bcard_id":business_card_response["data"]})
                      businesscard_copy['businesscard'][position]['json_data']=business_data
                  #------------------- End -----------------------------------------------#
                     
                  #-----------------  Update the business card ---------------------------# 
                  if raw_data["operation"] == 'update':                    
                    business_data = []
                    if raw_data["json_data"]:
                      #------------- execute all business card-----------------------#  
                      for items in raw_data["json_data"]:  
                            data = {}
                            data['user_id'] = user_id
                            try:
                              data['bcard_json_data'] = items['bcard_json_data']
                            except:
                              data['bcard_json_data'] =''
                            
                            #------------- Local business card id --------------#
                            try:
                              local_business_id = items['local_business_id']
                            except:
                              local_business_id =''  
                            #-------------------- End --------------------------#
                            
                            #------------- Local business card id --------------#
                            try:
                              data['bcard_id'] = items['bcard_id']
                            except:
                              data['bcard_id'] =''  
                            #-------------------- End --------------------------#                            
                            if data['bcard_id']:
                                business_card_response = business_card_class.update(request,None,1,data)
                                if business_card_response["status"]:
                                   try:
                                     bcard_id = business_card_response["data"]["id"]
                                   except:
                                     bcard_id = business_card_response["data"]  
                                   business_data.append({"local_business_id":local_business_id,"bcard_id":bcard_id})
                                else:
                                   business_data.append({"local_business_id":local_business_id,"bcard_id":business_card_response["data"]})
                            else:
                                business_data.append({"local_business_id":local_business_id,"bcard_id":'provide business card id to update'})
                      businesscard_copy['businesscard'][position]['json_data']=business_data    
                  position = position + 1
                  
              return CustomeResponse(businesscard_copy,status=status.HTTP_200_OK)
          
          
      @list_route(methods=['get'],)
      def receive(self, request):
          pass      


      @list_route(methods=["post"],)
      # update multiple settings in case of offline----------#
      def updatemultiplerecord(self,request):
          #data format {"DISPLAY_CONTACT_NAME_AS":"1","LANGUAGE":"1"} -------# 
         getkey  =request.DATA 
         updated_settings = []
         non_updated_settings = []
         for key,value in getkey.items(): 
                try:
                  UserSetting.objects.filter(user_id=request.user.id,setting_id__key=key).update(value=value)
                  updated_settings.append(key)
                except:
                  non_updated_settings.append(key)  
         return CustomeResponse({"updated_settings":updated_settings,"non_updated_settings":non_updated_settings}, status=status.HTTP_200_OK)
#        try:
#            getkey  =request.DATA
#
#            settingdata = Setting.objects.all()
#            usersettingdata = UserSetting.objects.all()
#            
#            usersettingexist = UserSetting.objects.filter(user_id=request.user.id)
#            if usersettingexist:
#            
#           # get corresponding key and setting id from setting table-----------#
#                tempContainer = []
#                count = 0
#                for i in getkey: 
#                    innerloop= 0
#                    for j in settingdata:
#                        data   = {}
#                        if i==j.key:
#                            data = {"key":j.key,"setting_id":j.id}
#                            datas = tempContainer.append(data)                        
#                            count=count+1
#            
#            # make dictionary for setting_id corresponding to key and its value to be update in usersetting table-------#
#            
#                newtempContainer = []
#                counter=0
#                for getdata in getkey:
#                    existingdata    =   0   
#                    for i in tempContainer:
#                        data    =   {}
#                        if getdata in i['key']:
#                            value   =  getkey[i['key']]
#                            data    =   {"setting_id":i['setting_id'],"value":value,"user_id":request.user.id}
#                            datas = newtempContainer.append(data)                        
#                            counter=counter+1
#
#            # update usersetting records corresponding to setting_id in usersetting table--------#
#                    j=0         
#                    for i in usersettingdata:
#                        for k in newtempContainer :
#                            if i.setting_id.id == k['setting_id'] and k['user_id']==i.user_id.id:
#                                UserSetting.objects.filter(user_id=request.user.id,setting_id=k['setting_id']).update(value=k['value'])
#                                j=j+1
#                                
#                if newtempContainer:
#                    return CustomeResponse({"msg":"Data has been updated"},status=status.HTTP_200_OK)
#                else:
#                    return CustomeResponse({"msg":" No Data found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#                        
#            else:
#                return CustomeResponse({"msg":" No Data found for this user"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#                                                                                     
#        except:
#            return CustomeResponse({"msg":"Data not found"},validate_errors=1)
          

#      @list_route(methods=['post'],)
#      def sendVactioncard(self,request):
#        try:
#            user_id    =   request.user
#        
#        except:
#            user_id     =   None
#        
#        
#        try:
#            vacation_card = request.data['vacationcard']
#            vacationcard_copy = request.data.copy()
#        except:
#            vacation_card = ''
#          
#        final_return_data = {}
#        
#        if vacation_card:  
#            vacation_card_class = VacationCardViewSet()
#            position = 0
#            for raw_data in vacation_card:
#                  if raw_data["operation"] == 'add':
#                    vacation_data = []
#                     #-----------------  Create the vacation card ---------------------------# 
#                    data = {}
#                    try:
#                        data['vacation_name'] = raw_data['vacation_name']
#                    except:
#                        data['vacation_name'] =''
#                    
#                    try:
#                        data['vacation'] =      raw_data['vacation']
#                    except:
#                        data['vacation'] =''
#                        
#                     
#                    vacation_card_response = vacation_card_class.create(request,1,data)
#                    print vacation_card_response
#                     
#                    if vacation_card_response["status"]:
#                            try:
#                                 vcard_id = vacation_card_response["data"]["id"]
#                            except:
#                                 vcard_id = vacation_card_response["data"]  
#                            vacation_data.append({"local_vacation_id":local_business_id,"bcard_id":bcard_id})
#                    else:
#                        vacation_data.append({"local_vacation_id":local_vacation_id,"vcard_id":vacation_card_response["data"]})
#            vacationcard_copy['vacationcard'][position]['vacation']=vacation_data    
#        position = position + 1   
#        return CustomeResponse(vacationcard_copy,status=status.HTTP_200_OK)    
            
#---------------------------- End ----------------------------------------------#

#---------------------------  Fetch data from server ---------------------------#


#---------------------------  End ----------------------------------------------#
