#----------------------------------------------#
# Developer Name: Sajid
# Creation Date: 2015/08/04
# Notes: View File
#----------------------------------------------#
from models import User,Profile,SocialLogin
from serializer import UserSerializer,ProfileSerializer,SocialLoginSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

import rest_framework.status as status

from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse
from ohmgear.auth_frontend import authenticate_frontend

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
import datetime
from datetime import timedelta
from django.utils.timezone import utc

from rest_framework import permissions 
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from functions import getToken,checkEmail
import json

#class UserPermissionsObj(permissions.BasePermission):
#    """
#    Object-level permission to only allow owners of an object to edit it.
#    Assumes the model instance has an `owner` attribute.    ##"""
#    def has_permission(self, request, view):
#        if request.method == 'POST':
#            return True
#        else:            
#            return True
# User View Prototype which will same format for other view
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_permissions(self):
        # Your logic should be all here
        if self.request.method == 'POST':
            self.authentication_classes = []
            self.permission_classes = []
        else:            
            self.authentication_classes = [ExpiringTokenAuthentication,]
            self.permission_classes = [IsAuthenticated, ]
        return super(viewsets.ModelViewSet, self).get_permissions()    

    def set_password(self,request,user_id):
      try:
        user = get_user_model().objects.get(id=user_id) 
        user.set_password(request.DATA['password'])
        user.save()
        return True
      except:
        return False  
    
    #---    -----------Method: GET-----------------------------#       
    def list(self, request):
         return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)   
    
    #--------------Method: GET retrieve single record-----------------------------#
    def retrive(self,request,pk=None):
        queryset = self.queryset
        user = get_object_or_404(queryset,pk=pk)
        serializer = self.serializer_class(user,context={'request':request})
        return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
    
    #--------------Method: POST create new user -----------------------------#
    def create(self, request,fromsocial=None):
         
         serializer =  UserSerializer(data=request.DATA,context={'request': request})
         if serializer.is_valid():
            user_id=serializer.save() 
            #---------------- Set the password -----------#
            if 'password' in request.DATA and request.DATA['password'] is not None:
               self.set_password(request,user_id.id)
            #---------------- End ------------------------#
            if not fromsocial:
             return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
            else:
             return serializer.data   
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
    #--------------Method: PUT update the record-----------------------------#
    def update(self, request, pk=None):
         try:
           messages = User.objects.get(id=pk)
         except:
           return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)
       
         serializer =  UserSerializer(messages,data=request.DATA,partial=True,context={'request': request})
         if serializer.is_valid():
            serializer.save()
            #---------------- Set the password -----------#
            if 'password' in request.DATA and request.DATA['password'] is not None:
               self.set_password(request,pk)
            #---------------- End ------------------------#            
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

    
    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        return CustomeResponse({'msg':'DELETE method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,flag=1)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    #--------------Method: GET-----------------------------#       
    def list(self,request):
         return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
 
    #--------------Method: GET retrieve single record-----------------------------#
    def retrieve(self, request,pk=None):
        queryset = self.queryset
        profile = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(profile,context={'request': request})
        return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
    
     #--------------Method: PUT update the record-----------------------------#
    def update(self, request, pk=None):
         try:
           messages = Profile.objects.get(id=pk)
         except:
           return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)
       
         serializer =  ProfileSerializer(messages,data=request.DATA,partial=True,context={'request': request})
         if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

    
    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,flag=1)

    
class SocialLoginViewSet(viewsets.ModelViewSet):     
    queryset = SocialLogin.objects.all()
    serializer_class = SocialLoginSerializer
    
    def create(self, request):    
                serializer =  UserSerializer(data=request.DATA,context={'request': request,'msg':'not exist'})
                try:               
                 user = checkEmail(request.DATA['email'])
                except:
                    user = ''
                if user:
                   #--------------- Create the token ------------------------#
                   try:
                    token = getToken(user[0]['id'])
                    user[0]['token'] = token
                   except:
                     pass
                   #---------------- End ------------------------------------# 
                   return CustomeResponse(user,status=status.HTTP_302_FOUND,already_exist=0,validate_errors=0)
                else:
                    if serializer.is_valid():
                        try:
                            #---------- Call the userviewset for create the user ------------#
                            user_view_obj = UserViewSet()
                            data = user_view_obj.create(request,1)
                            #----------- End ------------------------------------------------#
                            social_id = request.POST.get('social_id','')
                            sociallogin = SocialLogin(user_id=data['id'],social_media_login_id = social_id)                            
                            sociallogin.save()
                            #--------------- Create the token ------------------------#
                            try:                                
                                token = getToken(data['id'])
                                data['token'] =  token                           
                            except:
                                data['token'] = ''
                            #---------------- End ------------------------------------#
                            return CustomeResponse(data,status=status.HTTP_201_CREATED)
                        except:
                            return CustomeResponse({'msg':'provide required parameters'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                    else:
                       return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)


            
#----------User Login | Forgot Password | Reset Password -----------------#      
@api_view(['GET','POST'])       
def useractivity(request):
    msg = {}
    if request.method == 'GET':
     pass        
    if request.method == 'POST':
        op = request.POST.get('op','')
        # ----------- Login ------------------#
        if op == 'login':
                username = request.POST.get('username','')
                password = request.POST.get('password','')

                if username and password:
                    user = authenticate_frontend(username=username, password=password)
                    if user and not None:
                        if  user.status != 1:
                            msg = 'User account is disabled.'
                            return CustomeResponse({'msg':msg},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
                    else:
                        msg = 'Unable to log in with provided credentials.'
                        return CustomeResponse({'msg':msg},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
                        #raise exceptions.ValidationError(msg)
                else:
                    msg = 'Must include "username" and "password".'
                    return CustomeResponse({'msg':msg},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
                
                ###----------------- Create Token ---------------------------#
                #----------- everytime user login user will get new token ----#
                #----------- first check previus token if exist then delete -----------#
                user = model_to_dict(user)
                token = getToken(user["id"])
                user['token'] = token
                ###------------------ End -----------------------------------#
                return CustomeResponse(user,status=status.HTTP_200_OK)
        else:
             return CustomeResponse({'msg':'Please provide operation parameter op'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)            
