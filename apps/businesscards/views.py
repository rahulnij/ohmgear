from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import rest_framework.status as status

from models import BusinessCard,BusinessCardTemplate,BusinessCardIdentifier,Identifier
from serializer import BusinessCardSerializer,BusinessCardIdentifierSerializer
from apps.contacts.serializer import ContactsSerializer
from apps.contacts.models import Contacts

from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse,handle_uploaded_file
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION

from django.core.exceptions import ValidationError
import json,validictory
from django.shortcuts import get_object_or_404
from django.conf import settings
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
         
     

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)    
    
    
    def get_queryset(self):
        user_id = self.request.QUERY_PARAMS.get('user_id', None)
        published = self.request.QUERY_PARAMS.get('published', None)
        check = 0
        #---------------------- Filter ------------------------#
        if published is not None and user_id is not None:
            if published == '0':
              queryset = self.queryset.select_related('user_id').filter(user_id=user_id,status=0)
            elif published == '1':
              queryset = self.queryset.select_related('user_id').filter(user_id=user_id,status=1)
            check = 1  
        elif user_id is not None:
            queryset = self.queryset.select_related('user_id').filter(user_id=user_id)
            check = 1
        #------------------------- End -------------------------#  
        if check: 
         return queryset
        else:
         return None   

    #--------------Method: GET retrieve single record-----------------------------#
    def retrieve(self,request,pk=None,call_from_function=None):
        queryset = self.queryset
        user = get_object_or_404(BusinessCard,pk=pk)
        serializer = self.serializer_class(user,context={'request':request})
        if call_from_function:
            return serializer.data
        else:
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
    
    #--------------Method: POST create new business card -----------------------------#
    def create(self, request):
         
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
         
         #---------------------------- Duplicate the business card -------------------------------------#
         try:
           bcard_id = request.data["bcard_id"]
         except:
           bcard_id = None  
         if bcard_id:
            from functions import createDuplicateBusinessCard
            bcards_id_new = createDuplicateBusinessCard(bcard_id)
            data          =  self.retrieve(request,pk=bcards_id_new,call_from_function=1)
            return CustomeResponse(data,status=status.HTTP_200_OK)
         
         #----------------------------- End ------------------------------------------------------------#
         serializer =  BusinessCardSerializer(data=request.data,context={'request': request})
         if serializer.is_valid():
            contact_serializer =  ContactsSerializer(data=request.DATA,context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                #print contact_serializer.validated_data['businesscard_id']
                contact_serializer.validated_data['businesscard_id'] = business
                contact = contact_serializer.save()
                #-------------- Save Notes -------------------------------#
                data_new = serializer.data.copy()
                try:
                    if request.data['note_frontend']:
                                from apps.notes.views import NotesViewSet
                                note_view_obj = NotesViewSet()
                                request_new = request.DATA.copy()
                                request_new.DATA = {}
                                request_new.DATA["user_id"]=request.data['user_id']
                                request_new.DATA["contact_id"]=contact.id
                                request_new.DATA["note"]=request.data['note_frontend']
                                data = note_view_obj.create(request_new,call_from_function=1) 
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
                contact = contact_serializer.save()
                print contact.id
                #-------------- Save Notes -------------------------------#
                data_new = serializer.data.copy()
                #try:
                if request.data['note_frontend'] or request.data['note_backend']:                        
                                from apps.notes.views import NotesViewSet
                                from apps.notes.models import Notes
                                note_view_obj = NotesViewSet() 
                                request_new = request.DATA.copy()
                                request_new.DATA = {}
                                request_new.DATA["user_id"]=request.data['user_id']
                                request_new.DATA["contact_id"]=contact.id
                                if "note_frontend" in request.data and request.data['note_frontend']:
                                    request_new.DATA["note"]=request.data['note_frontend']
                                    try:
                                     note_id = Notes.objects.get(contact_id = contact.id,user_id = request.data['user_id'],bcard_side_no = 1)
                                    except:
                                     note_id = ""
                                    if note_id: 
                                        data = note_view_obj.update(request_new,pk=note_id.id,call_from_function=1)
                                    else:
                                        data = note_view_obj.create(request_new,call_from_function=1)
                                    data_new['note_frontend'] = request.data['note_frontend']
                                if "note_backend" in request.data and request.data['note_backend']:
                                    request_new.DATA["note"]=request.data['note_backend']
                                    try:
                                     note_id = Notes.objects.get(contact_id = contact.id,user_id = request.data['user_id'],bcard_side_no = 2)
                                    except:
                                     note_id = ""
                                    if note_id: 
                                        data = note_view_obj.update(request_new,pk=note_id.id,call_from_function=1)
                                    else:
                                        data = note_view_obj.create(request_new,call_from_function=1)
                                    data_new['note_backend'] = request.data['note_backend']                                    
                #except:
                #    pass                            
                #-------------------------End-----------------------------------#                
                
            else:
                return CustomeResponse(contact_serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
            return CustomeResponse(data_new,status=status.HTTP_201_CREATED)
 
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
        

    def destroy(self, request, pk=None):
         print pk
         try:
           bcards = BusinessCard.objects.get(id=pk)
           bcards.delete()
           return CustomeResponse({'msg':'record deleted'},status=status.HTTP_200_OK)
         except:
           return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)
