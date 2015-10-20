from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import rest_framework.status as status

from models import BusinessCard,BusinessCardTemplate
from serializer import BusinessCardSerializer
from apps.contacts.serializer import ContactsSerializer

from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION

from django.core.exceptions import ValidationError
import json,validictory
from django.shortcuts import get_object_or_404
# Create your views here.

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)    
    

    #---    -----------Method: GET-----------------------------#       
    def list(self, request):
         return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)   
    
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
         #---------------------- - End ----------------------------------------------------------- #
         
         #---------------------- Handle File Upload : Business card image  ----------------------------------------#
         try:
             bcard_image = request.FILES['bcard_image']
         except:
             bcard_image = ''
         if bcard_image:
             pass             
         #----------------------------------------------------------------------------------#
         serializer =  BusinessCardSerializer(data=request.DATA,context={'request': request})
         if serializer.is_valid():
            contact_serializer =  ContactsSerializer(data=request.DATA,context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact = contact_serializer.save(businesscard = business)
            else:
                return CustomeResponse(contact_serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
 
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
    def update(self, request, pk=None):  
         #-------------------- First Validate the json contact data ------------------------------#
         try:
            validictory.validate(json.loads(request.DATA["bcard_json_data"]), BUSINESS_CARD_DATA_VALIDATION)
         except validictory.ValidationError as error:
            return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
         except validictory.SchemaError as error:
            return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
         except:
            return CustomeResponse({'msg':"Please provide bcard_json_data in json format" },status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
         #---------------------- - End ----------------------------------------------------------- #
         
         
         serializer =  BusinessCardSerializer(data=request.DATA,context={'request': request})
         if serializer.is_valid():
            print request.DATA
            contact_serializer =  ContactsSerializer(data=request.DATA,context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact = contact_serializer.save(businesscard = business)
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