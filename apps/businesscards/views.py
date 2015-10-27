from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import rest_framework.status as status

from models import BusinessCard,BusinessCardTemplate
from serializer import BusinessCardSerializer
from apps.contacts.serializer import ContactsSerializer

from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse,handle_uploaded_file
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION

from django.core.exceptions import ValidationError
import json,validictory
from django.shortcuts import get_object_or_404
from django.conf import settings
# Create your views here.

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)    
    
    
#    def get_queryset(self):
#        queryset = self.queryset
#        user_id = self.request.QUERY_PARAMS.get('user_id', None)
#        if user_id is not None:
#           queryset = queryset.filter(user_id=user_id) 
#        return queryset

    #---    -----------Method: GET-----------------------------#       
    def list(self, request):
        user_id = self.request.QUERY_PARAMS.get('user_id', None)
        if user_id is not None:
            queryset = self.queryset.select_related('user').get(user_id=user_id)
            serializer = self.serializer_class(queryset,context={'request':request})
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)             
        else:
         return CustomeResponse({'msg':'GET method allowed with filters only'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)   
    
    #--------------Method: GET retrieve single record-----------------------------#
    def retrieve(self,request,pk=None):
        queryset = self.queryset
        user = get_object_or_404(BusinessCard,pk=pk)
        serializer = self.serializer_class(user,context={'request':request})
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
         
         
         serializer =  BusinessCardSerializer(data=request.DATA,context={'request': request})
         if serializer.is_valid():
            print request.DATA
            contact_serializer =  ContactsSerializer(data=request.DATA,context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact_serializer.validated_data['businesscard_id'] = business
                contact = contact_serializer.save()

                #-------------- Save Notes -------------------------------#
                data_new = serializer.data.copy()
                try:
                    if request.data['note_frontend']:
                                from apps.notes.views import NotesViewSet
                                from apps.notes.models import Notes
                                note_view_obj = NotesViewSet()
                                request_new = request.DATA.copy()
                                request_new.DATA = {}
                                request_new.DATA["id"]=Notes.objects.get()
                                request_new.DATA["user_id"]=request.data['user_id']
                                request_new.DATA["contact_id"]=contact.id
                                request_new.DATA["note"]=request.data['note_frontend']
                                data = note_view_obj.update(request_new,call_from_function=1) 
                                data_new['note_frontend'] = request.data['note_frontend']
                except:
                    pass                            
                #-------------------------End-----------------------------------#
                
            else:
                return CustomeResponse(contact_serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
 
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
        
#    #--------------Method: PUT update the record-----------------------------#
#    def update(self, request, pk=None):
#         try:
#           messages = User.objects.get(id=pk)
#         except:
#           return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)
#       
#         serializer =  UserSerializer(messages,data=request.DATA,partial=True,context={'request': request})
#         if serializer.is_valid():
#            serializer.save()
#            #---------------- Set the password -----------#
#            if 'password' in request.DATA and request.DATA['password'] is not None:
#               self.set_password(request,pk)
#            #---------------- End ------------------------#            
#            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#
#    
#    def partial_update(self, request, pk=None):
#        pass
#
#    def destroy(self, request, pk=None):
#        return CustomeResponse({'msg':'DELETE method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,flag=1)