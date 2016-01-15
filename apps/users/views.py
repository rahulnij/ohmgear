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
from django.shortcuts import redirect
import hashlib, datetime, random
from rest_framework.decorators import detail_route, list_route
from apps.usersetting.models import Setting
from apps.usersetting.serializer import UserSignupSettingSerializer
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
    def retrieve(self,request,pk=None):
        queryset = self.queryset
        user = get_object_or_404(queryset,pk=pk)
        serializer = self.serializer_class(user,context={'request':request})
        return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
    
    #--------------Method: POST create new user -----------------------------#
    def create(self, request,fromsocial=None):
         
         serializer =  UserSerializer(data=request.DATA,context={'request': request})
         if serializer.is_valid():
             
            #------------ enable/desable signal -----------------#
            if fromsocial:
                self._disable_signals = True
            #------------ End -----------------------------------#
            user_id=serializer.save() 
            
            #---------------- create the profile -----------#
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+user_id.email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            profile = Profile()
            profile.activation_key = activation_key
            profile.key_expires = key_expires
            profile.user_id = user_id.id
            
            if request.data.has_key('first_name'):
                profile.first_name = request.data['first_name']
                
            if request.data.has_key('last_name'):
                profile.last_name = request.data['last_name']
                
            profile.save()
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
#            #---------------- Set the password -----------#
#            if 'password' in request.DATA and request.DATA['password'] is not None:
#               self.set_password(request,pk)
#            #---------------- End ------------------------#            
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

    
    @list_route(methods=['post'],)   
    def changepassword(self,request):
        try:
            user_id =request.user.id
            old_password    =  request.DATA['old_password']
            password        =  request.DATA['password']
            confirmpassword =  request.DATA['confirm_password']
        except:
            return CustomeResponse({'msg':'Old_password,password and confirm_password are missing'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   
        
        userdata        = User.objects.filter(id=request.user.id).values()
        email            = userdata[0]['email']
        
        if old_password:
            user = authenticate_frontend(username=email, password=old_password)
            if user and not None:
                    if password == confirmpassword :
                        user = User.objects.get(id=user_id)
                        user.set_password(password)
                        user.update_password = False
                        user.save()
                        return CustomeResponse({'msg':"Password changed successfully"},status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse({'msg':"password and confirm password are not same"},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
            else:
                msg = 'Old Password is wrong'
                return CustomeResponse({'msg':msg},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
        else:
            msg = 'Must include "old_Password".'
            return CustomeResponse({'msg':msg},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
        
    def usersetting(self,request,user_id):
        try:
            settingvalue = Setting.objects.all()
            
            if settingvalue:
                    tempContainer = []
                    for data in settingvalue:
                        tempdata = {}
                        tempdata['user_id']= user_id
                        tempdata['setting_id'] = data.id
                        tempdata['value'] = data.value_type
                        tempContainer.append(tempdata)
                    print tempContainer
                    serializer = UserSignupSettingSerializer(data=tempContainer,many=True)
                    if serializer.is_valid():
                        serializer.save()
                        return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
                    else:
                        return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)
                        
        except:
            return CustomeResponse({'msg':'provide status active'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   


    
    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        return CustomeResponse({'msg':'DELETE method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,flag=1)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related().all()
    serializer_class = ProfileSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
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
    def create(self, request, pk=None):
        try:
            user_id = request.user.id
            messages = Profile.objects.get(user_id=user_id) 
            if request.data.has_key('profile_image'):
                  profile_image   = request.data['profile_image']
            else:
                 profile_image = messages.profile_image
        except:
           return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)
        serializer =  ProfileSerializer(messages,data=request.DATA,partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save(first_time_login  = False,profile_image= profile_image)
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
                try:
                  if request.DATA['status'] is 0:
                     return CustomeResponse({'msg':'provide status active'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
                except:
                  return CustomeResponse({'msg':'provide status active'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   
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
                   #print user
                   return CustomeResponse(user[0],status=status.HTTP_302_FOUND,already_exist=0,validate_errors=0)
                else:
                    if serializer.is_valid():
                        #try:
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
                        #except:
                            return CustomeResponse({'msg':'provide required parameters'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                    else:
                       return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)


            
#----------User Login | Forgot Password | Reset Password -----------------#      
@api_view(['GET','POST'])       
def useractivity(request,**kwargs):
    msg = {}
    print request.device
    if request.method == 'GET':
       activation_key = kwargs.get("activation_key")
       reset_password_key = kwargs.get("reset_password_key")
       
       #------------- get the activation key and activate the account : Process after registration ----------------------#
       if activation_key:
          #try: 
            user_profile = get_object_or_404(Profile, activation_key=activation_key)
            user = user_profile.user
            user.status = 1
            user.update_password = False
            user.save()
            user_setting = UserViewSet()
            user_setting.usersetting(request,user.id)
            if request.device:
                from django.http import HttpResponse
                #----------- token value and user_id for direct login into app ----------------------#
                token_value = getToken(user.id)
                response = HttpResponse("ohmgear://?token="+str(token_value), status=302)
                response['Location'] = "ohmgear://?token="+str(token_value)
                return response 
            else:
               return CustomeResponse('Account has been activated',status=status.HTTP_200_OK) 
         # except:
          #  return CustomeResponse({'msg':'Incorrect activation key'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1) 
       #------------------------------------ End --------------------------------------------------#
       
       #--------------------  Get the reset password key and redirect to mobile : Processed when forgot password mail link clicked----------------------#
       elif reset_password_key: 
            if request.device:
                from django.http import HttpResponse
                response = HttpResponse("ohmgear://?resetPasswordKey="+reset_password_key, status=302)
                response['Location'] = "ohmgear://?resetPasswordKey="+reset_password_key
                return response 
            else:                         
               return CustomeResponse({'msg':'This url is used in app only'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)               
       return CustomeResponse({'msg':'Please provide correct parameters'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)              
    
    if request.method == 'POST':
        op = request.POST.get('op','')
        # ----------- Login ------------------#
        if op == 'login':
                username = request.POST.get('username','')
                password = request.POST.get('password','')
                #------------------- save password in case of forgot passord ----------------#
                reset_password_key = request.POST.get('reset_password_key','')
                if reset_password_key:
                    try:
                     profile = Profile.objects.select_related().get(reset_password_key=reset_password_key,user__email=username)
                     profile.user.set_password(password)
                     profile.user.update_password = False
                     profile.user.save()
                    except:
                     return CustomeResponse({'msg':'There is problem in reset password'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
                
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
                try:
                 profile = Profile.objects.get(user_id=user["id"])
                 user['first_time_login'] = profile.first_time_login
                except:
                 pass   
                user['token'] = token
                ###------------------ End -----------------------------------#
                return CustomeResponse(user,status=status.HTTP_200_OK)
        # ----------- restet password and send the email------------------#
        elif op == 'reset_password':
            
                email = request.POST.get('email','')
                try:
                 profile = Profile.objects.select_related().get(user__email=request.DATA['email'],user__user_type__in=[2,3])
                except:
                 profile = ''
                if email:                   
                    
                    if profile and not None:
                        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                        reset_password_key = hashlib.sha1(salt+profile.user.email).hexdigest()
                        
                        from apps.email.views import BaseSendMail  
                        user = model_to_dict(profile.user)
                        BaseSendMail.delay(user,type='forgot_password',key = reset_password_key)                        
                        profile.reset_password_key = reset_password_key
                        profile.save()
                        return CustomeResponse(user,status=status.HTTP_200_OK)
                    else:
                        msg = 'This email id does not exist.'
                        return CustomeResponse({'msg':msg},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
                        #raise exceptions.ValidationError(msg)
                else:
                    msg = 'Must include "email".'
                    return CustomeResponse({'msg':msg},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)

                return CustomeResponse(profile,status=status.HTTP_200_OK)
            
        elif op == 'resend_register_mail':
            
                email = request.POST.get('email','')                
                try:
                 profile = Profile.objects.select_related().get(user__email=email)
                except:
                 profile = ''
                
                if profile:
                   from apps.email.views import BaseSendMail
                   user = model_to_dict(profile.user)
                   BaseSendMail.delay(user,type='account_confirmation',key = profile.activation_key)
                   return CustomeResponse({'msg':"email sent"},status=status.HTTP_200_OK)
                else:
                   return CustomeResponse({'msg':"email does not exist"},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1) 
                 
                 
            
        else:
             return CustomeResponse({'msg':'Please provide operation parameter op'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)            

