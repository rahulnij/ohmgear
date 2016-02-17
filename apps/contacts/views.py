#--------- Import Python Modules -----------#
import json,jsonschema
import validictory
from collections import OrderedDict
#-------------------------------------------#
#------------ Third Party Imports ----------#
from django.shortcuts import render
import rest_framework.status as status
from rest_framework.decorators import api_view
from rest_framework.decorators import detail_route, list_route
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
#-------------------------------------------#
#------------------ Local app imports ------#
from ohmgear.functions import CustomeResponse
from serializer import ContactsSerializer,ContactsSerializerWithJson
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION
from models import Contacts
from ohmgear.token_authentication import ExpiringTokenAuthentication
from apps.businesscards.views import BusinessViewSet

from apps.folders.views import FolderViewSet
from apps.folders.models import Folder
from apps.folders.serializer import FolderContactSerializer
#---------------------------End------------------------------------#


#--------------------- Storing Contacts as a Bulk -----------------------#
class storeContactsViewSet(viewsets.ModelViewSet):
    
      queryset = Contacts.objects.all()
      serializer_class = ContactsSerializer
      authentication_classes = (ExpiringTokenAuthentication,)
      permission_classes = (IsAuthenticated,)      
      
      def list(self,request):
        queryset = self.queryset.filter(user_id=request.user.id) 
        serializer = self.serializer_class(queryset,many=True)
        
        if serializer.data:
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg":"No Data found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=True)
        
      def create(self, request):
          return CustomeResponse({'msg':'POST method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
      
      @list_route(methods=['post'],)
      def uploads(self, request):
             
             user_id = request.user
             NUMBER_OF_CONTACT = 100
             
             try:
              contact = request.DATA['contact']
             except:
               return CustomeResponse({'msg':'Please provide correct Json Format'},status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
            
             if contact:
               counter = 0  
               #---------------- Assign  first created business card to created default folder -----#
               queryset_folder = Folder.objects.filter(user_id=user_id,foldertype='PR').values()
               if not queryset_folder:
                    folder_view = FolderViewSet.as_view({'post': 'create'})
                    offline_data={}
                    offline_data['businesscard_id'] =''   
                    offline_data['foldername'] = 'PR'
                    folder_view= folder_view(request,offline_data)
                    folder_id = folder_view.data['data']['id']
               else:
                    folder_id = queryset_folder[0]['id']
     
               #-------------------- End --------------------------------------------------------#               
               contact_new = []
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
                    if 'user_id' not in contact_temp:
                        contact_temp['user_id'] = user_id.id
                        contact_new.append(contact_temp)
                    else:
                        contact_new.append(contact_temp) 
                    counter = counter + 1
                    
               if counter > NUMBER_OF_CONTACT:
                    return CustomeResponse({'msg':"Max "+str(NUMBER_OF_CONTACT)+" allowed to upload"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
               
               
               serializer = ContactsSerializer(data=contact_new,many=True)
               if serializer.is_valid():
                    serializer.save()
                    #-------------------- Assign all contacts to folder -----------------#
                    folder_contact_array = []
                    
                    for items in serializer.data:
                        folder_contact_array.append({'user_id':user_id.id,'folder_id':folder_id,'contact_id':items['id']})
  
                    if  folder_contact_array:
                            folder_contact_serializer = FolderContactSerializer(data=folder_contact_array,many=True)
                            if folder_contact_serializer.is_valid():
                               folder_contact_serializer.save() 
                    #--------------------------- End ------------------------------------#
                    
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
          
               """ TODO : check optimization """
               first_name = []
               last_name = []               
               email = []
               phone = []
               
               try:
                  first_name=[value['value'] for  value in first_json["side_first"]["basic_info"] if value['keyName'] == 'FirstName']
               except:
                  pass
              
               try:
                  last_name=[value['value'] for  value in first_json["side_first"]["basic_info"] if value['keyName'] == 'LastName']
               except:
                  pass              
              
               try:
                  email = first_json["side_first"]["contact_info"]["email"].values()
               except:
                  pass 
                
               try:    
                  phone = first_json["side_first"]["contact_info"]["phone"].values()
               except:
                  pass
               
               try:
                  email.append(first_json["side_second"]["contact_info"]["email"].values())
               except:
                  pass
              
               try:
                  phone.append(first_json["side_second"]["contact_info"]["phone"].values())                  
               except:
                  pass
              

               first_name_target = []
               last_name_target = [] 
               email_target = []
               phone_target = []
               
               try:
                  first_name_target=[value['value'] for  value in second_json["side_first"]["basic_info"] if value['keyName'] == 'FirstName']
               except:
                  pass
              
               try:
                  last_name_target=[value['value'] for  value in second_json["side_first"]["basic_info"] if value['keyName'] == 'LastName']
               except:
                  pass                
               
               try:
                   email_target = second_json["side_first"]["contact_info"]["email"].values()
               except:
                   pass
               
               try:
                   phone_target = second_json["side_first"]["contact_info"]["phone"].values()
               except:
                   pass
               try:
                   email_target.append(second_json["side_second"]["contact_info"]["email"].values())
               except:
                   pass
               try:
                   phone_target.append(second_json["side_second"]["contact_info"]["phone"].values())                  
               except:
                   pass                

               check_duplicate_1 = 0
               for first_name_val in first_name:
                   if first_name_val in first_name_target and first_name_val != []:
                        check_duplicate_1 = 1 
               
               if not check_duplicate_1:         
                for last_name_val in last_name:
                    if last_name_val in last_name_target and last_name_val != []:
                         check_duplicate_1 = 1                

               check_duplicate_2 = 0
               for email_val in email:
                   if email_val in email_target and email_val != []:
                        check_duplicate_2 = 1
                        
               if not check_duplicate_2:
                for phone_val in phone:
                    if phone_val in phone_target and phone_val != []:
                         check_duplicate_2 = 1 

               # Condition {First_Name OR Last_Name} AND {email OR phone OR instant_message}
               if check_duplicate_1 and check_duplicate_2:
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
               
               try:           
                  user_id = request.user.id
               except:
                  user_id = None            
               try:
                  merge_contact_ids = request.data["merge_contact_ids"]
                  target_contact_id = request.data["target_contact_id"]
               except:
                  merge_contact_ids = None
                  target_contact_id = None
                  
               #------------------ Get the  target_bcard_id and merge_bcards_ids data ------------------------------#
               if merge_contact_ids and target_contact_id and user_id:
                    
                    try:
                       target_contact = Contacts.objects.get(id=target_contact_id,user_id= user_id)
                    except:
                       return CustomeResponse({"msg":"target_contact_id does not exist"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                   
                    first_json = json.loads(json.dumps(target_contact.bcard_json_data))
                    #---- make sure target_bcard_id not in merge_bcards_ids ---------------------------------------------#
                    if target_contact_id not in merge_contact_ids:
                    #-----------------------------------------------------------------------------------------------------#                    
                        merge_contacts = Contacts.objects.filter(id__in=merge_contact_ids,user_id= user_id).exclude(businesscard_id__isnull=False).all()
                        for temp in merge_contacts:
                            contact_json_data = temp.bcard_json_data
                            if contact_json_data:
                               try: 
                                second_json = json.loads(json.dumps(contact_json_data))
                               except:
                                second_json = {}   
                               third_json = second_json.copy()
                               card_object = BusinessViewSet()
                               card_object.mergeDict(third_json, first_json)
                               
                               #------ assign the new json ----------------------------#
                               target_contact.bcard_json_data = third_json
                               target_contact.save(force_update=True)
                               first_json = third_json
                        if merge_contacts:
                            #pass
                            merge_contacts.delete()
                        else:
                           return CustomeResponse({"msg":"merge_contact_ids does not exist OR merge contact links with business card"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
                        #----------------------- End ---------------------------------------------#
                        return CustomeResponse({"msg":"successfully merged"},status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse({"msg":"Please provide correct target_contact_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
               else:
                    return CustomeResponse({"msg":"Please provide merge_contact_ids, target_contact_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
          
              
          
          