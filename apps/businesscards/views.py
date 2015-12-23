from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import rest_framework.status as status

from models import BusinessCard,BusinessCardTemplate,BusinessCardIdentifier,Identifier,BusinessCardMedia,BusinessCardSkillAvailable,BusinessCardAddSkill,BusinessCardHistory

from serializer import BusinessCardSerializer,BusinessCardIdentifierSerializer,BusinessCardMediaSerializer,BusinessCardSkillAvailableSerializer,BusinessCardAddSkillSerializer,BusinessCardSummarySerializer,BusinessCardHistorySerializer

from apps.contacts.serializer import ContactsSerializer
from apps.contacts.models import Contacts
from apps.identifiers.models import Identifier
from apps.identifiers.serializer import IdentifierSerializer
from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse,handle_uploaded_file
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION

from django.core.exceptions import ValidationError
import json,validictory
from django.shortcuts import get_object_or_404
from django.conf import settings
from apps.users.models import User
from apps.vacationcard.models import VacationCard 
from apps.vacationcard.serializer import VacationCardSerializer
import itertools
from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route
import collections    
#---------------- Business Card Summary ----------------------#
class CardSummary(APIView):
    """
    View to card summary.
    """
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BusinessCard.objects.all()
    
    def get(self, request):
        bcard_id = self.request.QUERY_PARAMS.get('bcard_id', None)
        if bcard_id:
           queryset = self.queryset.filter(id=bcard_id) 

           serializer = BusinessCardSummarySerializer(queryset,many=True)
           dt = serializer.data
           for d in serializer.data:
                dt = d
                businesscard =  BusinessCard(id=bcard_id)
                dt['business_media'] =  businesscard.bcard_image_frontend()
                break
           return CustomeResponse(dt,status=status.HTTP_200_OK)
        else:
           return CustomeResponse({'msg':'GET method not allowed without business card id'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1) 
    def post(self, request, format=None):
        return CustomeResponse({'msg':'POST method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
#---------------------- End ----------------------------------#


# Create your views here.

class BusinessCardIdentifierViewSet(viewsets.ModelViewSet):
    queryset  = BusinessCardIdentifier.objects.all()
    serializer_class = BusinessCardIdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
     #--------------Method: GET-----------------------------#       
    def list(self,request):

            user_id  =request.user
            self.queryset = Identifier.objects.all().filter(user_id=user_id)
            """
            get all identifiers from identifiers table
            """
            serializer = IdentifierSerializer(self.queryset,many=True)
            if serializer: 
                    return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
            else:
                return CustomeResponse({'msg':"No Data Found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
           
           
            
    def create(self,request):
       #print request.data
        try:
            op  =request.DATA['op']
        except:
           op = None
        if op == 'change':
            businesscard_id  = request.DATA['businesscard_id']
        
            if businesscard_id:
               businesscardidentifier_detail = BusinessCardIdentifier.objects.filter(businesscard_id= businesscard_id)
               businesscardidentifier_detail.delete()
       
       
        serializer = BusinessCardIdentifierSerializer(data = request.data,context={'request':request})
        if serializer.is_valid():
           serializer.save()
           BusinessCard.objects.filter(id= request.data['businesscard_id']).update(status= 1 )
           return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
           return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
    def update(self, request, pk=None):
        
           getidentifierid = BusinessCardIdentifier.objects.filter(id=pk).values()
           identifierid =  getidentifierid[0]['identifier_id_id']
          
           #------Unlink Identifier status 0 in identifier table--------#
           #Identifier.objects.filter(id=identifierid).update(status=0 )
           #------Unlink Businesscard Identifier status 0 in Bsuinesscardidentifier table--------#
           BusinessCardIdentifier.objects.filter(id=pk).update(status=0 )
           return CustomeResponse({'msg':"Business card has been unlinked with identifiers "},status=status.HTTP_200_OK)
       
     
    #-------Delete Identifiers it will first inactive the businesscard than delete the linking of identifier with businesscard in businesscard_identifier table
     #than delete the identifeirs in identifier table ------------# 
    def destroy(self, request, pk=None):
        businesscard_identifier = BusinessCardIdentifier.objects.filter(id=pk)

        if businesscard_identifier:
            businesscard_id = businesscard_identifier[0].businesscard_id.id
            identifier_id   = businesscard_identifier[0].identifier_id_id
            BusinessCard.objects.filter(id=businesscard_id).update(status=0 )
            Identifier.objects.filter(id=identifier_id).delete()
            businesscard_identifier.delete()   
            return CustomeResponse({'msg':"Business card has been Inactive and identifiers has been deleted "},status=status.HTTP_200_OK)
        else:
             return CustomeResponse({'msg':"Businesscard Identifier Id not found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                            
            
    
         
# BusinessCard Gallery 
class BusinessCardMediaViewSet(viewsets.ModelViewSet):
    queryset  = BusinessCardMedia.objects.all().order_by('front_back')
    serializer_class = BusinessCardMediaSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
    
    def list(self,request):
            user_id = self.request.user.id
            bcard_id = self.request.QUERY_PARAMS.get('bcard_id', None) 
            if bcard_id:
                #-------- Should be pass queryset to serializer but error occured ---#
                self.queryset = self.queryset.filter(businesscard_id=bcard_id,user_id=user_id)
                if self.queryset: 
                    data = {}
                    data['all'] = []
                    data['top'] = []
                    i = 0 
                    for items in self.queryset:
                        print items
                        if items.status == 1:
                           data['top'].append({"image_id":items.id,"front_back":items.front_back,"img_url":str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(items.img_url)})
                        data['all'].append({"image_id":items.id,"front_back":items.front_back,"img_url":str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(items.img_url)})
                    return CustomeResponse(data,status=status.HTTP_200_OK)
                else:
                   return CustomeResponse({'msg':"Data not exist"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            else:
                return CustomeResponse({'msg':"Without parameters does not support"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                            
            
    #------------- Add image into business card gallary ---------------------#
    def create(self,request,call_from_function=None):
        data = request.data.copy()
        data['status'] = 0 
        data['user_id'] = self.request.user.id
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
    #----------------- End-------------------------------------------------------#
    #------------- Upload image after business card created ---------------------#
    @list_route(methods=['post'],) 
    def upload(self,request):
        user_id = self.request.user.id
        bcard_id = self.request.data["bcard_id"] 
        try:
          business = BusinessCard.objects.get(id=bcard_id,user_id=user_id)   
        except:
         return CustomeResponse({'msg':"Business id does not exist"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   
        #-------------- Save Image in image Gallary -------------------------------#
        data_new = {}
        data_new['bcard_image_frontend'] = ""
        data_new['bcard_image_backend'] = ""
        try:
         if 'bcard_image_frontend' in request.data and  request.data['bcard_image_frontend']: 
           #------------------ Set previous image 0 ----------------------------------------# 
           BusinessCardMedia.objects.filter(businesscard_id=business,front_back=1).update(status=0)
           bcard_image_frontend, created = BusinessCardMedia.objects.update_or_create(user_id=self.request.user,businesscard_id=business,img_url=request.data['bcard_image_frontend'],front_back=1,status=1)
           #print bcard_image_frontend.img_url
           data_new['bcard_image_frontend'] = str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(bcard_image_frontend.img_url)                  
        except:
           pass

        try:
         if 'bcard_image_backend' in request.data and  request.data['bcard_image_backend']:
           BusinessCardMedia.objects.filter(businesscard_id=business,front_back=2).update(status=0)  
           bcard_image_backend, created = BusinessCardMedia.objects.update_or_create(user_id=self.request.user,businesscard_id=business,img_url=request.data['bcard_image_backend'],front_back=2,status=1)
           if bcard_image_backend:
              data_new['bcard_image_backend'] = str(settings.DOMAIN_NAME)+str(settings.MEDIA_URL)+str(bcard_image_backend.img_url)                  

        except:
            pass 
            
        if data_new['bcard_image_frontend'] or data_new['bcard_image_backend']:
           return CustomeResponse({"bcard_id":bcard_id,"bcard_image_frontend":data_new['bcard_image_frontend'],"bcard_image_backend":data_new['bcard_image_backend']},status=status.HTTP_201_CREATED)
        else:
           return CustomeResponse({'msg':"Please upload media bcard_image_frontend or bcard_image_backend"},status=status.HTTP_200_OK)     
        #-------------------------End-----------------------------------#        
    #-------------------- Change image of business card -----------------------#
    @list_route(methods=['post'],) 
    def change(self,request):
        user_id = request.user.id
        try:
          bcard_id = request.data["bcard_id"]
          gallary_image_id = request.data["gallary_image_id"]
          image_type = request.data["image_type"] # means it is 1 frontend or 2 backend 
        except:
          bcard_id = None  
          
        if bcard_id:
          try:  
           get_image = BusinessCardMedia.objects.get(id=gallary_image_id,businesscard_id=bcard_id,user_id=user_id)
           get_image.status = 1
           get_image.front_back = image_type
           get_image.save()
           BusinessCardMedia.objects.filter(businesscard_id=bcard_id,front_back=image_type).exclude(id=gallary_image_id).update(status=0)
           return CustomeResponse({"msg":"Business card image changed successfully."},status=status.HTTP_200_OK)
          except:
            return CustomeResponse({'msg':"provided bcard_id,gallary_image_id not valid"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  
        else:
          return CustomeResponse({'msg':"Please provide bcard_id,gallary_image_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  
    #------------------------------ End ---------------------------------------#
        
    def update(self, request, pk=None):
         return CustomeResponse({'msg':"Update method does not allow"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    
    def destroy(self, request, pk=None):
        try:
            user_id = request.user.id
            bcard_id = request.data["bcard_id"]
            get_image = BusinessCardMedia.objects.get(id=pk,businesscard_id=bcard_id,user_id=user_id,status=1)
            #get_image.delete()
            return CustomeResponse({'msg':"Media deleted successfully"},status=status.HTTP_200_OK)
        except:
            return CustomeResponse({'msg':"Please provide correct bcard_id,media id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  

#BusinessCard History

class BusinessCardHistoryViewSet(viewsets.ModelViewSet):
    queryset  = BusinessCardHistory.objects.all()
    serializer_class = BusinessCardHistorySerializer
    #authentication_classes = (ExpiringTokenAuthentication,)
    #permission_classes = (IsAuthenticated,) 
     #--------------Method: GET-----------------------------#   
        
    def list(self,request):
            bid = self.request.QUERY_PARAMS.get('bid', None)
            if bid:
               self.queryset = self.queryset.filter(businesscard_id=bid).order_by('updated_date').values()
               
               if self.queryset: 
                    data = {}
                    data['side_first'] = []
                    data['side_second'] = []
                    
                    #for items in self.queryset:
                     #   data['side_first'].append({"bcard_json_data":items['bcard_json_data']['side_first']['basic_info']})
                      #  data['side_second'].append({"bcard_json_data":items['bcard_json_data']['side_second']['contact_info']})
                        #print data
            serializer = self.serializer_class(self.queryset,many=True)
            if serializer: 
                    return CustomeResponse(self.queryset,status=status.HTTP_200_OK)
            else:
               return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
  
    def create(self,request):
        serializer = BusinessCardHistorySerializer(data = request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
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
               self.queryset = self.queryset.filter(skill_name__istartswith=skill)
            serializer = self.serializer_class(self.queryset,many=True)
            if serializer and self.queryset: 
                    return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
            else:
               return CustomeResponse({'msg':'no data found'},status=status.HTTP_200_OK,validate_errors=1)
  
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
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
     #--------------Method: GET-----------------------------#       
    def list(self,request):
        return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)

    def retrieve(self,request,pk=None):
        return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
    
    def create(self,request):
      #  tempData = request.data.copy()]
        tempData = {}
        tempData['user_id'] = request.user.id
        tempData['businesscard_id'] = request.DATA['businesscard_id']
        tempData['skill_name'] = request.DATA['skill_name'].split(',')
        serializer = BusinessCardAddSkillSerializer(data = tempData,context={'request':request})

        if serializer.is_valid():
            #request.POST._mutable = True
            businesscard_id = tempData['businesscard_id']
            user_id = tempData['user_id']
            skill_name = tempData['skill_name']
    
            #update = request.POST.get('update')
            BusinessCardAddSkill.objects.filter(businesscard_id=businesscard_id).delete()
            for item in skill_name:
                data = {}
                data['skill_name'] = item
                data['user_id'] = user_id
                data['businesscard_id'] = businesscard_id
                serializer = BusinessCardAddSkillSerializer(data = data,context={'request':request})
                serializer.is_valid()
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
        
        #user_id = self.request.QUERY_PARAMS.get('user_id', None)
        user_id = request.user.id
        published = self.request.QUERY_PARAMS.get('published', None)
        business_id = self.request.QUERY_PARAMS.get('business_id', None)
        is_active   = self.request.QUERY_PARAMS.get('is_active',None)
        vacation_data_check = 0
        #---------------------- Filter ------------------------#
        if published is not None and user_id is not None:
            if published == '0':
              self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id,status=0,is_active=1)
            elif published == '1':
              self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id,status=1,is_active=1)
        
        elif is_active is not None and user_id is not None:
            self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id,is_active=0,status=0)
        
        elif user_id is not None and business_id == 'all':
                #----------------- All user business card -------------------------------------#
                self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id)  
                self.vacation_data = VacationCard.objects.all().filter(user_id=user_id)
                vacation_data_check = 1
        elif user_id is not None:
            self.queryset = self.queryset.select_related('user_id').filter(user_id=user_id)
        
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
        user_id = request.user.id
        bcard_obj = get_object_or_404(BusinessCard,pk=pk,user_id=user_id)
        serializer = self.serializer_class(bcard_obj,context={'request':request})
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
    def create(self, request): 
         try:
           op = request.data["op"]
         except:             
           op = None
           
         try:           
           user_id = request.user.id
         except:
           user_id = None  
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
         tempData = request.data.copy()
         tempData["user_id"] = user_id
         
         serializer =  BusinessCardSerializer(data=tempData,context={'request': request})
         if serializer.is_valid():
            contact_serializer =  ContactsSerializer(data=tempData,context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact_serializer.validated_data['businesscard_id'] = business
                contact_serializer.save()
                contact = Contacts.objects.get(businesscard_id=business.id)
                user = User.objects.get(id=user_id)
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
         data = request.DATA.copy()
         user_id  =request.user.id
         data['user_id']  =request.user.id
         try:
           bcards = BusinessCard.objects.get(id=pk)
         except:
           return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)         
         
         serializer =  BusinessCardSerializer(bcards,data=data,context={'request': request})
         if serializer.is_valid():
            contact = Contacts.objects.get(businesscard_id=pk) 
            contact_serializer =  ContactsSerializer(contact,data=data,context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact_new = contact_serializer.save()
                user = User.objects.get(id=user_id)
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
            else:
                return CustomeResponse(contact_serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
            return CustomeResponse(data_new,status=status.HTTP_200_OK)
 
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
        
    #---------------------------- Duplicate the business card ----------------------------#
    @list_route(methods=['post'],)   
    def duplicate(self,request):
            try:           
              user_id = request.user.id
            except:
              user_id = None 
              
            try:
                  bcard_id = request.data["bcard_id"]     
            except:
                  bcard_id = None
                  
            if bcard_id and user_id:
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
    def mergeDict(self,s, f):
        for k, v in f.iteritems():
            if isinstance(v, collections.Mapping):
                r = self.mergeDict(s.get(k, {}), v)
                s[k] = r
            elif isinstance(v, list):
                result = []
                """ TODO : optimization """
                
                if k == 'basic_info':
                   for  valf in v:
                        if 'keyName' in valf:
                            for vals in s.get(k, {}):
                                    if valf['keyName'] in vals.values() and vals['value'] !="" and valf['value'] == "":
                                        valf['value'] = vals['value']
                            result.append(valf)
                   """ Reverse loop is for check  extra data in second business card """          
                   for vals1 in s.get(k, {}):
                           if 'keyName' in vals1:
                              check = 0  
                              for valf1 in v:
                                  if vals1['keyName'] in valf1.values():
                                     check = 1
                              if not check:
                                  result.append(vals1)                            
                else:
                   v.extend(s.get(k, {})) 
                   for myDict in v:
                        if myDict not in result:
                            result.append(myDict)
                                  
                s[k] = result    
            else:
                #------------- If the key is blank in first business card then second business card value assign to it -----#
                if not v and s.get(k, {}):
                    #f[k] = s.get(k, {})
                    pass
                else:    
                    s[k] = f[k]
        return s
    
    @list_route(methods=['post'],)   
    def merge(self,request):
#               first_json = {"basic_info":[{"indexPos": "0", "isUpper": "1", "placeHolder": "NAME THIS CARD (Required)", "value": "ddd", "keyName": "CardName"},{"indexPos": "0", "isUpper": "1", "placeHolder": "NAME THIS CARD (Required)sddd", "value": "", "keyName": "CardName11"}]}
#               second_json = {"basic_info": [{"indexPos": "0", "isUpper": "1", "placeHolder": "NAME THIS CARD (Required)sddd", "value": "wwwwwwwwww", "keyName": "CardName"},{"indexPos": "0", "isUpper": "1", "placeHolder": "NAME THIS CARD (Required)sddd", "value": "dsfsdfd", "keyName": "CardName11"}]}
#               third_json = second_json.copy()
#               self.mergeDict(third_json, first_json)
#               print third_json
#               return CustomeResponse({"msg":"Please provide bcard_id and user_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)            
#              
               try:           
                  user_id = request.user.id
               except:
                  user_id = None            
               try:
                  merge_bcards_ids = request.data["merge_bcards_ids"]
                  target_bcard_id = request.data["target_bcard_id"]
               except:
                  merge_bcards_ids = None
                  target_bcard_id = None
                  
               #------------------ Get the  target_bcard_id and merge_bcards_ids data ------------------------------#
               if merge_bcards_ids and target_bcard_id and user_id:
                    target_bacard = BusinessCard.objects.select_related().get(id=target_bcard_id,user_id= user_id)
                    first_json = json.loads(json.dumps(target_bacard.contact_detail.bcard_json_data))
                    #---- make sure target_bcard_id not in merge_bcards_ids ---------------------------------------------#
                    if target_bcard_id not in merge_bcards_ids:
                    #-----------------------------------------------------------------------------------------------------#                    
                        merge_bcards = BusinessCard.objects.filter(id__in=merge_bcards_ids,user_id= user_id).all()

                        for temp in merge_bcards:
                            contact_json_data = temp.contact_detail.bcard_json_data
                            if contact_json_data:
                               try: 
                                second_json = json.loads(json.dumps(contact_json_data))
                               except:
                                second_json = {}   
                               third_json = second_json.copy()

                               self.mergeDict(third_json, first_json)
                               #------ assign the new json ----------------------------#
                               target_bacard.contact_detail.bcard_json_data = third_json
                               target_bacard.contact_detail.save(force_update=True)
                               first_json = third_json
                        #------------------- TODO Delete the  merge_bcards_ids -------------------#
                        if merge_bcards:
                            #pass
                            merge_bcards.delete()
                        else:
                           return CustomeResponse({"msg":"merge_bcards_ids does not exist."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
                        #----------------------- End ---------------------------------------------#
                        return CustomeResponse({"msg":"successfully merged"},status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse({"msg":"Please provide correct target_bcard_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
               else:
                    return CustomeResponse({"msg":"Please provide merge_bcards_ids, target_bcard_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
    #----------------------------- End ----------------------------------------------------#      
    
    #---------------------------- Delete business card -------------------------------------#    
    @list_route(methods=['post'],)   
    def delete(self,request):
                
                try:           
                  user_id = request.user.id
                except:
                  user_id = None        
                try:
                 bcard_ids = request.data["bcard_ids"]
                except:
                 bcard_ids = None
                 
                if bcard_ids and user_id:
                    try:
                     business_card = BusinessCard.objects.filter(id__in=bcard_ids,user_id= user_id)
                     if business_card:
                       business_card.delete()   
                       return CustomeResponse({"msg":"business card deleted successfully."},status=status.HTTP_200_OK)
                     else:
                       return CustomeResponse({"msg":"business card does not exists."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  
                    except:
                     return CustomeResponse({"msg":"some problem occured on server side during delete business cards"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
    #----------------------------- End ----------------------------------------------------#
    
    #---------------------------- Inactive Business Card -------------------------------------#        
    @list_route(methods=['post'],)   
    def inactive(self,request):
               
               try:           
                  user_id = request.user.id
               except:
                  user_id = None        
               try:
                   bcards_id = request.DATA["bcards_ids"]
               except:
                   bcards_id = None
               if bcards_id:
                   try:
                     businesscard = BusinessCard.objects.filter(id__in=bcards_id,user_id=user_id).update(is_active=0,status=0)
                     return CustomeResponse({"msg":"Business cards has been inactive"},status=status.HTTP_200_OK)
                   except:
                     return CustomeResponse({"msg":"some problem occured on server side during inactive business cards"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)           
               else:
                     return CustomeResponse({"msg":"please provide bcards_ids for inactive businesscard"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
                  
    #------------------------------- End ---------------------------------------------------#           
    def destroy(self, request, pk=None):
         return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)
