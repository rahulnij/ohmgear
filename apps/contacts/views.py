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
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated

class storeContactsViewSet(viewsets.ModelViewSet):
    
      queryset = Contacts.objects.all()
      serializer_class = ContactsSerializer
      authentication_classes = (ExpiringTokenAuthentication,)
      permission_classes = (IsAuthenticated,)      
      
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
      
      def find_duplicate(self,first_json,second_json):
               
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
                   if email_val in email_target and email_val != []:
                        check_duplicate = 1
                        
               if not check_duplicate:
                for phone_val in phone:
                    if phone_val in phone_target and phone_val != []:
                         check_duplicate = 1 

               if check_duplicate:
                  return 1
               else:
                  return 0 
      
      @list_route(methods=['post'],)
      def get_duplicate_contacts(self, request):
          user_id  = request.user.id
          contacts = list(self.queryset.filter(user_id=user_id).values('id','businesscard_id','bcard_json_data').order_by("id"))
          contacts_copy = contacts
          #------------------- fetch contact json detail from qeuryset -----------------------------#
          
          finalContacts = []
          count = 0
          duplicate_contacts_ids = []
          inner_loop = 0
          
          for value in contacts: 
               check = 1
               duplicateContacts = []
               iterator = iter(contacts_copy)
               try :
                 while 1:
                     value_copy = iterator.next() 

                     if value["id"] != value_copy["id"] and value["id"] not in duplicate_contacts_ids:
                        result = self.find_duplicate(value["bcard_json_data"],value_copy["bcard_json_data"])
                        if result:
                           if check == 1:
                              finalContacts.append(value)
                              inner_loop = inner_loop + 1
                              check = 0
                           duplicateContacts.append(json.loads(json.dumps(value_copy)))
                           duplicate_contacts_ids.append(value_copy["id"])
               except StopIteration, e :
                      if count == inner_loop-1: 
                         finalContacts[inner_loop-1]["duplicate"]=duplicateContacts
                      
                      
               
               count = count + 1
                          
               
          return CustomeResponse(finalContacts,status=status.HTTP_200_OK)
      
      
      @list_route(methods=['post'],)
      def merge(self,request):
                pass
#               try:           
#                  user_id = request.user.id
#               except:
#                  user_id = None            
#               try:
#                  merge_bcards_ids = request.data["merge_contact_ids"]
#                  target_bcard_id = request.data["target_contact_id"]
#               except:
#                  merge_bcards_ids = None
#                  target_bcard_id = None
#                  
#               #------------------ Get the  target_bcard_id and merge_bcards_ids data ------------------------------#
#               if merge_bcards_ids and target_bcard_id and user_id:
#                    target_bacard = BusinessCard.objects.select_related().get(id=target_bcard_id,user_id= user_id)
#                    first_json = json.loads(json.dumps(target_bacard.contact_detail.bcard_json_data))
#                    #---- make sure target_bcard_id not in merge_bcards_ids ---------------------------------------------#
#                    if target_bcard_id not in merge_bcards_ids:
#                    #-----------------------------------------------------------------------------------------------------#                    
#                        merge_bcards = BusinessCard.objects.filter(id__in=merge_bcards_ids,user_id= user_id).all()
#                        
#                        for temp in merge_bcards:
#                            contact_json_data = temp.contact_detail.bcard_json_data
#                            if contact_json_data:
#                               try: 
#                                second_json = json.loads(json.dumps(contact_json_data))
#                               except:
#                                second_json = {}   
#                               third_json = second_json.copy()
#
#                               self.mergeDict(third_json, first_json)
#                               
#                               #------ assign the new json ----------------------------#
#                               target_bacard.contact_detail.bcard_json_data = third_json
#                               target_bacard.contact_detail.save(force_update=True)
#                               first_json = third_json
#                        #------------------- TODO Delete the  merge_bcards_ids -------------------#
#                        if merge_bcards:
#                            #pass
#                            merge_bcards.delete()
#                        else:
#                           return CustomeResponse({"msg":"merge_bcards_ids does not exist."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
#                        #----------------------- End ---------------------------------------------#
#                        return CustomeResponse({"msg":"successfully merged"},status=status.HTTP_200_OK)
#                    else:
#                        return CustomeResponse({"msg":"Please provide correct target_bcard_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
#               else:
#                    return CustomeResponse({"msg":"Please provide merge_bcards_ids, target_bcard_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
          
              
          
          