from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import rest_framework.status as status

from models import BusinessCard,BusinessCardTemplate,BusinessCardIdentifier,Identifier,BusinessCardMedia,BusinessCardSkillAvailable,BusinessCardAddSkill
from serializer import BusinessCardSerializer,BusinessCardIdentifierSerializer,BusinessCardMediaSerializer,BusinessCardSkillAvailableSerializer,BusinessCardAddSkillSerializer
from apps.contacts.serializer import ContactsSerializer
from apps.contacts.models import Contacts

from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse,handle_uploaded_file
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION

from django.core.exceptions import ValidationError
import validictory
from django.shortcuts import get_object_or_404
from django.conf import settings
from apps.users.models import User
from apps.vacationcard.models import VacationCard 
from apps.vacationcard.serializer import VacationCardSerializer
import simplejson as json
# Create your views here.

class BusinessCardIdentifierViewSet(viewsets.ModelViewSet):
    queryset  = BusinessCardIdentifier.objects.all()
    serializer_class = BusinessCardIdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
     #--------------Method: GET-----------------------------#       
    def list(self,request):
        return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
 
    
    def create(self,request):
       serializer = BusinessCardIdentifierSerializer(data = request.data,context={'request':request})
       if serializer.is_valid():
           serializer.save()
           return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
       else:
           return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
    def update(self, request, pk=None):
        
           getidentifierid = BusinessCardIdentifier.objects.filter(id=pk).values()
           identifierid =  getidentifierid[0]['identifier_id']
          
           #------Unlink Identifier status 0 in identifier table--------#
           Identifier.objects.filter(id=identifierid).update(status=0 )
           #------Unlink Businesscard Identifier status 0 in Bsuinesscardidentifier table--------#
           BusinessCardIdentifier.objects.filter(id=pk).update(status=0 )
           return CustomeResponse({'msg':"Business card Identifiers has deleted"},status=status.HTTP_200_OK)
         
# BusinessCard Gallery 
class BusinessCardMediaViewSet(viewsets.ModelViewSet):
    queryset  = BusinessCardMedia.objects.all()
    serializer_class = BusinessCardMediaSerializer
  
    def list(self,request):
            bcard_id = self.request.QUERY_PARAMS.get('bcard_id', None) 
            if bcard_id:
                #-------- Should be pass queryset to serializer but error occured ---#
                self.queryset = self.queryset.filter(businesscard_id=bcard_id)
                if self.queryset: 
                    data = {}
                    data['all'] = []
                    data['top'] = []
                    i = 0 
                    for items in self.queryset:
                        if items.status == 1:
                           data['top'].append({"front_back":items.front_back,"img_url":str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(items.img_url)})
                        data['all'].append({"front_back":items.front_back,"img_url":str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(items.img_url)})
                    return CustomeResponse(data,status=status.HTTP_200_OK)
                else:
                   return CustomeResponse({'msg':"Data not exist"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            else:
                return CustomeResponse({'msg':"Without parameters does not support"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                            
            
  
    def create(self,request,call_from_function=None):
        data = request.data.copy()
        data['status'] = 0 
        serializer = BusinessCardMediaSerializer(data = data,context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            if call_from_function:
               return json.loads(unicode(serializer.data))
            else:
               return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED) 
        else:
            if call_from_function:
               return serializer.errors
            else:
              return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
    def update(self, request, pk=None):
         return CustomeResponse({'msg':"Update method does not allow"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

#BusinessCard Available Skills

class BusinessCardSkillAvailableViewSet(viewsets.ModelViewSet):
    queryset  = BusinessCardSkillAvailable.objects.all()
    serializer_class = BusinessCardSkillAvailableSerializer
    #authentication_classes = (ExpiringTokenAuthentication,)
    #permission_classes = (IsAuthenticated,) 
     #--------------Method: GET-----------------------------#   
        
    def list(self,request):
            skill = self.request.QUERY_PARAMS.get('skill', None)
            if skill:
               self.queryset = self.queryset.filter(skill_name=skill)
            serializer = self.serializer_class(self.queryset,many=True)
            if serializer: 
                    return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
            else:
               return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
  
    def create(self,request):
        serializer = BusinessCardSkillAvailableSerializer(data = request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

        
        
    def update(self, request, pk=None):
         return CustomeResponse({'msg':"Update method does not allow"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
       
 # Add Skills to Business Card      
class BusinessCardAddSkillViewSet(viewsets.ModelViewSet):
    queryset  = BusinessCardAddSkill.objects.all()
    serializer_class = BusinessCardAddSkillSerializer
    #authentication_classes = (ExpiringTokenAuthentication,)
    #permission_classes = (IsAuthenticated,) 
     #--------------Method: GET-----------------------------#       
    def list(self,request):
        return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)

    def retrieve(self,request,pk=None):
        return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
    
    def create(self,request):
        serializer = BusinessCardAddSkillSerializer(data = request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

             
    def update(self, request, pk=None):
         return CustomeResponse({'msg':"Update method does not allow"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                  
     
class BusinessViewSet(viewsets.ModelViewSet):
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)    
    vacation_data = ''
    
   
    def list(self,request):
        
        user_id = self.request.QUERY_PARAMS.get('user_id', None)
        published = self.request.QUERY_PARAMS.get('published', None)
        business_id = self.request.QUERY_PARAMS.get('business_id', None)
        vacation_data_check = 0
        #---------------------- Filter ------------------------#
        if published is not None and user_id is not None:
            if published == '0':
              self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id,status=0)
            elif published == '1':
              self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id,status=1)
        elif user_id is not None and business_id == 'all':
                #----------------- All user business card -------------------------------------#
                self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id)  
                self.vacation_data = VacationCard.objects.all().filter(user_id=user_id)
                vacation_data_check = 1
        elif user_id is not None:
            self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id)
            check = 1
        
        #------------------------- End -------------------------#
        serializer = self.serializer_class(self.queryset,many=True)

        if vacation_data_check:
             data = {}
             data['business_cards'] = serializer.data
             data['vacation_cards'] =""            
             vacation_data = []
             for item in self.vacation_data:
                 vacation_data.append({"id":item.id,"user_id":item.user_id.id})
             data['vacation_cards'] = vacation_data
             return CustomeResponse(data,status=status.HTTP_200_OK)
        else:
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
         
    
    #--------------Method: GET retrieve single record-----------------------------#
    def retrieve(self,request,pk=None,call_from_function=None):
        queryset = self.queryset
        user = get_object_or_404(BusinessCard,pk=pk)
        serializer = self.serializer_class(user,context={'request':request})
        media=BusinessCardMedia.objects.filter(businesscard_id=pk,front_back__in=[1,2],status=1).values('img_url','front_back')
        data = {}
        data = serializer.data
        if media:
           try: 
            for item in media:
                if item['front_back'] == 1:
                         data['bcard_image_frontend'] = str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(item['img_url'])
                elif item['front_back'] == 2:
                         data['bcard_image_backend'] = str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(item['img_url'])
           except:
               pass
                        
        if call_from_function:
            return data
        else:
            return CustomeResponse(data,status=status.HTTP_200_OK)
    
    #--------------Method: POST create new business card and other operation -----------------------------#
    key_text = ''
    new_dict = {}
    key_store = []
    
    def get_value(self,d, k, i):
     print d,k,i   
     if isinstance(d[k[i]], str):
        return d[k[i]]
     return self.get_value(d[k[i]], k, i+1)    
    
    def checkItems(self,first=None,second=None):
                if isinstance(first, dict):
                    for key, item in first.iteritems():
                        
                          if isinstance(item, dict):
                            self.key_store.append(key)
                            #print self.new_dict,self.key_store
                            #print self.get_value(self.new_dict,self.key_store,0)
                            self.checkItems(item,self.get_value(self.new_dict,self.key_store,0))                       
                        
                          if not key in second:
                             second[key] = first[key]
                        
                print  second             
                          
    def create(self, request): 
         #---------------------------- Duplicate the business card ----------------------------#
         try:
           bcard_id = request.data["bcard_id"]     
         except:
           bcard_id = None
           
         try:
           op = request.data["op"]
         except:             
           op = None
           
         try:           
           user_id = request.data["user_id"] 
         except:
           user_id = None
           
         if op == 'duplicate':   
            if bcard_id and user_id:
               #----------------- Check that  bcard_id blongs to user -----------------#
               #--------------------------- End ---------------------------------------#
               from functions import createDuplicateBusinessCard
               bcards_id_new = createDuplicateBusinessCard(bcard_id,user_id)
               if bcards_id_new:
                 data =  self.retrieve(request,pk=bcards_id_new,call_from_function=1)
               else:
                   return CustomeResponse({"msg":"some problem occured on server side."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
               return CustomeResponse(data,status=status.HTTP_200_OK)
            else:
               return CustomeResponse({"msg":"Please provide bcard_id and user_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
         
         #----------------------------- End ----------------------------------------------------#
         
         #---------------------------- Merge business card -------------------------------------#
         try:
           merge_bcards_ids = request.data["merge_bcards_ids"]
           target_bacard_id = request.data["target_bacard_id"]
         except:
           merge_bcards_ids = None
           target_bacard_id = None
                   
         if op == 'merge':
            from functions import DiffJson            
            first = json.loads('{"first_name": "Poligraph", "last_name": {"saaa1":"de1","saaa2":{"dde":"e4e"}}}') 
            second = json.loads('{"first_name": "Poligraphovich", "last_name": {"saaa1":"de1","saaa2":{"dde":"e4e"}}}')
            
            self.new_dict = second
            self.checkItems(first,second) 
            print self.key_store
            if merge_bcards_ids and target_bacard_id and user_id:
                return True   
            else:
                return CustomeResponse({"msg":"Please provide merge_bcards_ids, target_bacard_id, user_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
            
         #----------------------------- End ----------------------------------------------------#
         
         #---------------------------- Delete Business Card -------------------------------------#         
         if op == 'delete':
             try:
              bcard_ids = request.data["bcard_ids"]
             except:
              bcard_ids = None
             if bcard_ids and user_id:
                 #try:
                  business_card = BusinessCard.objects.filter(id__in=[19],user_id= user_id)
                  if business_card:
                    business_card.delete()   
                    return CustomeResponse({"msg":"business card deleted successfully."},status=status.HTTP_200_OK)
                  else:
                    return CustomeResponse({"msg":"business card does not exists."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  
                 #except:
                  #return CustomeResponse({"msg":"some problem occured on server side during delete business cards"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)           
                 
         
         
         #------------------------------- End ---------------------------------------------------#
         
         #-------------------- First Validate the json contact data ------------------------------#
#         try:
#            validictory.validate(json.loads(request.DATA["bcard_json_data"]), BUSINESS_CARD_DATA_VALIDATION)
#         except validictory.ValidationError as error:
#            return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#         except validictory.SchemaError as error:
#            return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#         except:
#            return CustomeResponse({'msg':"Please provide bcard_json_data in json format" },status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
         #---------------------------------- End ----------------------------------------------------------- #
         
         serializer =  BusinessCardSerializer(data=request.data,context={'request': request})
         if serializer.is_valid():
            contact_serializer =  ContactsSerializer(data=request.DATA,context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact_serializer.validated_data['businesscard_id'] = business
                contact_serializer.save()
                contact = Contacts.objects.get(businesscard_id=business.id)
                user = User.objects.get(id=request.data['user_id'])
                #-------------- Save Notes -------------------------------#
                data_new = serializer.data.copy()
                try:
                    if request.data['note_frontend']:
                                from apps.notes.models import Notes                                
                                data = Notes.objects.update_or_create(user_id=user,contact_id=contact,note=request.data['note_frontend'],bcard_side_no=1) 
                                data_new['note_frontend'] = request.data['note_frontend']
                except:
                    pass                            
                #-------------------------End-----------------------------------#  
                
                #-------------- Save Image in image Gallary -------------------------------#
                try:
                 if 'bcard_image_frontend' in request.data and  request.data['bcard_image_frontend']: 
                   #------------------ Set previous image 0 ----------------------------------------# 
                   BusinessCardMedia.objects.filter(user_id=user,businesscard_id=business,front_back=1).update(status=0)
                   bcard_image_frontend, created = BusinessCardMedia.objects.update_or_create(user_id=user,businesscard_id=business,img_url=request.data['bcard_image_frontend'],front_back=1,status=1)
                   #print bcard_image_frontend.img_url
                   data_new['bcard_image_frontend'] = str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(bcard_image_frontend.img_url)                  
                except:
                   data_new['bcard_image_frontend'] = ""
                
                try:
                 if 'bcard_image_backend' in request.data and  request.data['bcard_image_backend']:
                   BusinessCardMedia.objects.filter(user_id=user,businesscard_id=business,front_back=2).update(status=0)  
                   bcard_image_backend, created = BusinessCardMedia.objects.update_or_create(user_id=user,businesscard_id=business,img_url=request.data['bcard_image_backend'],front_back=2,status=1)
                   if bcard_image_frontend:
                      data_new['bcard_image_backend'] = str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(bcard_image_backend.img_url)                  
                      pass
                except:
                    pass                
                
                #-------------------------End-----------------------------------#                  
                
            else:
                return CustomeResponse(contact_serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
            return CustomeResponse(data_new,status=status.HTTP_201_CREATED)
 
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
    def update(self, request, pk=None):  
         #-------------------- First Validate the json contact data ------------------------------#
#         try:
#            validictory.validate(json.loads(request.DATA["bcard_json_data"]), BUSINESS_CARD_DATA_VALIDATION)
#         except validictory.ValidationError as error:
#            return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#         except validictory.SchemaError as error:
#            return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#         except:
#            return CustomeResponse({'msg':"Please provide bcard_json_data in json format" },status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
         #---------------------- - End ----------------------------------------------------------- #
         try:
           bcards = BusinessCard.objects.get(id=pk)
         except:
           return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)         
         
         serializer =  BusinessCardSerializer(bcards,data=request.DATA,context={'request': request})
         if serializer.is_valid():
            contact = Contacts.objects.get(businesscard_id=pk) 
            contact_serializer =  ContactsSerializer(contact,data=request.DATA,context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact_new = contact_serializer.save()
                user = User.objects.get(id=request.data['user_id'])
                #-------------- Save Notes -------------------------------#
                data_new = serializer.data.copy()
                try:
                    if request.data['note_frontend'] or request.data['note_backend']:
                                    
                                    from apps.notes.models import Notes
                                    if "note_frontend" in request.data and request.data['note_frontend']:                                    
                                        data = Notes.objects.update_or_create(user_id=user,contact_id=contact,note=request.data['note_frontend'],bcard_side_no=1) 
                                        data_new['note_frontend'] = request.data['note_frontend']
                                    if "note_backend" in request.data and request.data['note_backend']:
                                        data = Notes.objects.update_or_create(user_id=user,contact_id=contact,note=request.data['note_frontend'],bcard_side_no=2) 
                                        data_new['note_backend'] = request.data['note_backend']                                    
                except:
                    pass                            
                #-------------------------End-----------------------------------# 
                
                #-------------- Save Image in image Gallary -------------------------------#
                try:
                 if 'bcard_image_frontend' in request.data and  request.data['bcard_image_frontend']: 
                   #------------------ Set previous image 0 ----------------------------------------# 
                   BusinessCardMedia.objects.filter(businesscard_id=business,front_back=1).update(status=0)
                   bcard_image_frontend, created = BusinessCardMedia.objects.update_or_create(user_id=user,businesscard_id=business,img_url=request.data['bcard_image_frontend'],front_back=1,status=1)
                   #print bcard_image_frontend.img_url
                   data_new['bcard_image_frontend'] = str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(bcard_image_frontend.img_url)                  
                except:
                   data_new['bcard_image_frontend'] = ""
                
                try:
                 if 'bcard_image_backend' in request.data and  request.data['bcard_image_backend']:
                   BusinessCardMedia.objects.filter(businesscard_id=business,front_back=2).update(status=0)  
                   bcard_image_backend, created = BusinessCardMedia.objects.update_or_create(user_id=user,businesscard_id=business,img_url=request.data['bcard_image_backend'],front_back=2,status=1)
                   if bcard_image_backend:
                      data_new['bcard_image_backend'] = str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(bcard_image_backend.img_url)                  
                      
                except:
                    data_new['bcard_image_backend'] = ""                
                
                #-------------------------End-----------------------------------#                 
                
                
            else:
                return CustomeResponse(contact_serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
            return CustomeResponse(data_new,status=status.HTTP_200_OK)
 
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
        

    def destroy(self, request, pk=None):
         return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)

