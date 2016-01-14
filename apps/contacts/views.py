from django.shortcuts import render
import rest_framework.status as status
import json,jsonschema
from rest_framework.decorators import api_view
from ohmgear.functions import CustomeResponse

from serializer import ContactsSerializer,ContactsSerializerWithJson
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION
import validictory
from models import Contacts
from rest_framework.decorators import detail_route, list_route
# Create your views here.

#--------------------- Storing Contacts as a Bulk -----------------------#
from rest_framework import viewsets

class storeContactsViewSet(viewsets.ModelViewSet):
    
      queryset = Contacts.objects.all()
      serializer_class = ContactsSerializer
      
      def list(self,request):
          return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
      
      def create(self, request):
          return CustomeResponse({'msg':'POST method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
      
      @list_route(methods=['post'],)
      def uploads(self, request):

             NUMBER_OF_CONTACT = 100
             try:
              contact = request.DATA['contact']
             except:
               return CustomeResponse({'msg':'Please provide correct Json Format'},status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
            
             if contact:
               counter = 0  
               for contact_temp in contact:
#                    print contact_temp
#                    #--------------------  Validate the json data ------------------------------#
#                    try:
#                       validictory.validate(contact_temp["bcard_json_data"], BUSINESS_CARD_DATA_VALIDATION)
#                    except validictory.ValidationError as error:
#                       return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#                    except validictory.SchemaError as error:
#                       return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
#                    ---------------------- - End ----------------------------------------------------------- #
                    counter = counter + 1
                    
               if counter > NUMBER_OF_CONTACT:
                    return CustomeResponse({'msg':"Max "+str(NUMBER_OF_CONTACT)+" allowed to upload"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
               serializer = ContactsSerializer(data=contact,many=True)
               if serializer.is_valid():
                serializer.save()
                return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
               else:
                return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)   
      
      def update(self, request, pk=None):
         return CustomeResponse({'msg':"Update method does not allow"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)      
      
      def destroy(self, request, pk=None):
          return CustomeResponse({'msg':'DELETE method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
      
      
      def merge_contacts(self,request):
          pass
      
      @list_route(methods=['post'],)
      def get_duplicate_contacts(self, request):
          user_id  = 2
          queryset = list(self.queryset.filter(user_id=user_id).values('id','businesscard_id','bcard_json_data'))
          #------------------- fetch contact json detail from qeuryset -----------------------------#
          
          finalContacts = []
          count = 1
          
          for value in queryset:

               #first_json = {"side_second": {"contact_info": {"website": {}, "name": {}, "title": {}, "social": {}, "phone": {"work":"999999","home":"88888888"}, "address": {}, "message": {}, "email": {"work":"sazid.se@gmail.com","home":"sazidk@clavax.us"}}},"side_first": {"contact_info": {"website": {"work": "hg.work.com", "home": "jhj.home.com", "other": "kk.other.com", "homepage": "hh.wwkk.jj"},"phone": {"home": "123456456789", "work": "797845645321", "iPhone": "145645646646"},"email": {"work": "asdfsadf@afsdf.dsf", "home": "home@home.com", "other": "my@normal.com", "iCloud": "asdfs@icloud.com"}} } }
               #second_json = {"side_second": {"contact_info": {"website": {}, "name": {}, "title": {}, "social": {}, "phone": {"work":"9919999","home":"888818888"}, "address": {}, "message": {}, "email": {"work":"sazid.se11@gmail.com","home":"sazidk11@clavax.us"}}},"side_first": {"contact_info": {"website": {"work": "hg.work.com", "home": "jhj.home.com", "other": "kk.other.com", "homepage": "hh.wwkk.jj"},"phone": {"home": "1234564567819", "work": "7978456145321", "iPhone": "145645646646"},"email": {"work": "asdfsadf@afsdf.11dsf", "home": "home@11home.com", "other": "my11@normal.com", "iCloud": "asdfs11@icloud.com"}} } }
               
               first_json = value['bcard_json_data']
               second_json = queryset[count]['bcard_json_data']
               
               email = []
               phone = []
               
               try:
                   email = first_json["side_first"]["contact_info"]["email"].values()
                   phone = first_json["side_first"]["contact_info"]["phone"].values()
                   email.append(first_json["side_second"]["contact_info"]["email"].values())
                   phone.append(first_json["side_second"]["contact_info"]["phone"].values())                  
               except:
                   pass
               
               
               email_target = []
               phone_target = []
               try:
                   email_target = second_json["side_first"]["contact_info"]["email"].values()
                   phone_target = second_json["side_first"]["contact_info"]["phone"].values()
                   email_target.append(second_json["side_second"]["contact_info"]["email"].values())
                   phone_target.append(second_json["side_second"]["contact_info"]["phone"].values())                  
               except:
                   pass                
               
               check_duplicate = 0
               for email_val in email:
                   if email_val in email_target:
                        check_duplicate = 1
                        
               if not check_duplicate:
                for phone_val in phone:
                    if phone_val in phone_target:
                         check_duplicate = 1   
                         
               if check_duplicate:
                   return CustomeResponse({'msg':"duplicate Found"},status=status.HTTP_200_OK)
               
               count = count + 1        
               #third_json = second_json.copy()
               #self.mergeDict(third_json, first_json)
               #print third_json
          
          return CustomeResponse({'msg':"dddd"},status=status.HTTP_200_OK)
              
          
          