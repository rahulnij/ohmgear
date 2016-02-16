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
from apps.businesscards.views import BusinessViewSet,BusinessCardIdentifierViewSet
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

             
          businesscard_copy = request.data.copy()    
          if 'businesscard' in request.data:
              
              businesscard = request.data['businesscard']
              
              business_card_class_create = BusinessViewSet.as_view({'post': 'create'})
              business_card_class_update = BusinessViewSet.as_view({'post': 'update'})
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
                            
                            business_card_response = business_card_class_create(request,1,data)
                            business_card_response = business_card_response.data
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
                                business_card_response = business_card_class_update(request,None,1,data)
                                business_card_response = business_card_response.data
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
          
          # Link identifier to business card
          # data format {"link_bcard_to_identifier":[{},{}]}
          if 'link_bcard_to_identifier' in request.data:
              
             link_bcard_to_identifier = request.data['link_bcard_to_identifier'] 
             link_bcard_to_identifier_class =  BusinessCardIdentifierViewSet()
             bcard_link_data = []
             for items in  link_bcard_to_identifier:
                 #data = {}
                 items['user_id'] = user_id
                 
                 response = link_bcard_to_identifier_class.create(request,1,items)
                 if response["status"]:
                    bcard_link_data.append({"msg":"atached"})
                 else:
                    bcard_link_data.append({"item":items,"msg":response}) 
                    
             businesscard_copy['link_bcard_to_identifier']=bcard_link_data  
                  
          return CustomeResponse(businesscard_copy,status=status.HTTP_200_OK)
          

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


      @list_route(methods=['post'],)

      def sendVactionCard(self,request):
      # data format {"vacationcard": [{"operation": "add","json_data": [{"vacation_name":"Us vacation123","vacation": [{"country":"ankurgumber","vacation_type":"confrence","contact_no":"8800362589","state":"Haryana","city":"gzb","notes":"hsfdjdfjfsed","trip_start_date":"2015-08-10","trip_end_date":"2015-11-28"}]}, {}]}, {	"operation": "update","json_data": [{}, {}]}] }  
        try:
            user_id    =   request.user.id
        
        except:
            user_id     =   None
        
        try:
            vacation_card = request.data['vacationcard']
            vacationcard_copy = request.data.copy()
        except:
            vacation_card = ''
            vacationcard_copy = ''
          
        final_return_data = {}
        
        if vacation_card:
              vacation_card_class = VacationCardViewSet() 
              position = 0
              for raw_data in vacation_card:
                  #i=0
                  #-----------------  Create the Vacation card ---------------------------#
                  if raw_data["operation"] == 'add': 
                    vacation_data = []
                    if raw_data["json_data"]:
                      #------------- execute all vacation card-----------------------#  
                      vcard_data=[]
                      stop_data = []
                      for items in raw_data["json_data"]:
                            data = {}
                            data['user_id'] = user_id
                            try:
                              data['vacation_name'] = items['vacation_name']
                            except:
                              data['vacation_name'] =''
                            
                            #------------- Local vacation card id --------------#
                            try:
                                    data['vacation'] =      items['vacation']
                            except:
                                    data['vacation'] =''
                            #-------------------- End --------------------------#
                            try:
                              local_vacation_id = items['local_vacation_id']
                            except:
                              local_vacation_id ='' 
                            
                            
                            vacation_card_response = vacation_card_class.create(request,1,data)
                            #print vacation_card_response
                            if vacation_card_response["status"]:
                               try:
                                 
                                 #stop ={}
                                 stop_id = vacation_card_response["data"][0]["id"]
                                 #stop = stop_id
                                 #stop_data.append(stop)
                                 vcard ={}
                                 vcard_id = vacation_card_response["data"][0]["vacationcard_id"]
                                 #vcard= vcard_id
                                 #vcard_data.append(vcard)
                                 vcard.append(vcard_id)
                               except:         
                                 vcard_id = vacation_card_response["data"]
                                         
                               vacation_data.append({"local_vacation_id":local_vacation_id,"vcard_id":vcard_id})
                            else:
                               
                               vacation_data.append({"local_vacation_id":local_vacation_id,"vcard_id":vacation_card_response["data"]})
                            #i=i+1
                      vacationcard_copy['vacationcard'][position]['json_data']=vacation_data
                  #------------------- End -----------------------------------------------#
                  
                  
                  #-----------------  Update the vacation card ---------------------------# 
                  if raw_data["operation"] == 'update':                    
                    vacation_data = []
                    if raw_data["json_data"]:
                      #------------- execute all vacation card-----------------------#  
                      for items in raw_data["json_data"]:

                            data = {}
                            data['user_id'] = user_id
                            try:
                              data['vacation_name'] = items['vacation_name']
                            except:
                              data['vacation_name'] =''
                            
                            #------------- Local vacation card id --------------#
                            try:
                                    data['vacation'] =      items['vacation']
                            except:
                                    data['vacation'] =''
                            
                                     
                            #------------- Local vacation card id --------------#
                            try:
                              local_vacation_id = items['local_vacation_id']
                            except:
                              local_vacation_id =''  
                            #-------------------- End --------------------------#
                            
                            #------------- Local vacation card id --------------#
                            try:
                              data['vcard_id'] = items['vcard_id']
                            except:
                              data['vcard_id'] =''  
                            #-------------------- End --------------------------#                            
                            if data['vcard_id']:
                                vacation_card_response = vacation_card_class.update(request,None,1,data)
                                if vacation_card_response["status"]:
                                    
                                   try:
                                     vcard ={}
                                     vcard_id = vacation_card_response["data"][0]["vacationcard_id"]
                                     #vcard= vcard_id
                                     #vcard_data.append(vcard)
                                     vcard.append(vcard_id)  
                                     #vcard_id = vacation_card_response["data"]["id"]
                                   except:
                                     vcard_id = vacation_card_response["data"]  
                                   vacation_data.append({"local_vacation_id":local_vacation_id,"vcard_id":vcard_id})
                                else:
                                   vacation_data.append({"local_vacation_id":local_vacation_id,"vcard_id":vacation_card_response["data"]})
                            else:
                                vacation_data.append({"local_business_id":local_vacation_id,"vcard_id":'provide vacation card id to update'})
                      vacationcard_copy['vacationcard'][position]['json_data']=vacation_data
                     

                  position = position + 1                  
        return CustomeResponse(vacationcard_copy,status=status.HTTP_200_OK)
        
        
        
        
        
#---------------------------- End ----------------------------------------------#


#---------------------------  Fetch data from server ---------------------------#
      @list_route(methods=['get'],)
      def receive(self, request):
          pass  

#---------------------------  End ----------------------------------------------#
