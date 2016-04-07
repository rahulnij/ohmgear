#----------------------------------------------#
# Developer Name: Sajid
# Creation Date: 2015/08/04
# Notes: View File
#----------------------------------------------#
from models import User,Profile,SocialLogin, SocialType,ConnectedAccount,UserEmail
from serializer import UserSerializer,ProfileSerializer,SocialLoginSerializer,ConnectedAccountsSerializer,UserEmailSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

import rest_framework.status as status

from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse
import ohmgear.settings.constant as constant
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
from functions import getToken,checkEmail,createConnectedAccount,CreatePinNumber
import json
from django.shortcuts import redirect
import hashlib, datetime, random
from rest_framework.decorators import detail_route, list_route
from apps.usersetting.models import Setting
from apps.usersetting.serializer import UserSignupSettingSerializer
import os
from django.conf import settings
from apps.email.views import BaseSendMail
from apps.businesscards.models import BusinessCard
from apps.businesscards.views import BusinessViewSet

from apps.businesscards.views import WhiteCardViewSet
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
        user.set_password(request.data['password'])
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
         
         serializer =  UserSerializer(data=request.data,context={'request': request})
         mutable = request.POST._mutable
         request.POST._mutable = True
         pin_no   =    CreatePinNumber()
         request.data['pin_number']  = pin_no
        
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
            
            #------------------------ grey contact invite auth-token -----------------------------#

            if request.GET.get('from_web', ''):
                token = getToken(user_id.id)
                cid = request.data['cid']
                sid = request.data['sid']
                from apps.sendrequest.models import SendRequest 
                SendRequest.objects.filter(sender_user_id=sid,receiver_obj_id=cid).update(read_status=1,receiver_user_id=user_id.id)
                business_card_class_create = WhiteCardViewSet.as_view({'post': 'create'})
    
                business_card_response = business_card_class_create(request,from_white_contact=user_id.id,cid=cid)
    
                #return CustomeResponse({"msg":business_card_response.data},status=status.HTTP_200_OK)    

            
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
       
         serializer =  UserSerializer(messages,data=request.data,partial=True,context={'request': request})
         if serializer.is_valid():
            serializer.save()
#            #---------------- Set the password -----------#
#            if 'password' in request.data and request.data['password'] is not None:
#               self.set_password(request,pk)
#            #---------------- End ------------------------#            
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

    
    @list_route(methods=['post'],)   
    def changepassword(self,request):
        try:
            user_id =request.user.id
            old_password    =  request.data['old_password']
            password        =  request.data['password']
            confirmpassword =  request.data['confirm_password']
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
        
    #------------------------Connects account of user i.e FB or Linkedin#---------    
    
    @list_route(methods=['get'],)
    def getConnectedAccounts(self,request):
        try:
            user_id = request.user
        except:
            user_id = None
        data ={}
        user_id  = request.user.id
        userConnectedData = ConnectedAccount.objects.select_related("social_type_id").filter(user_id=user_id)
        
        if userConnectedData:
                serializer = ConnectedAccountsSerializer(userConnectedData,many=True)
                return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse({'msg':"Data not found"},validate_errors=1)
    
    @list_route(methods=['post'],)
    def connectedaccounts(self,request):
        social_type =  constant.SOCIAL_TYPE
        social_type_exist =social_type.has_key(request.data['social_type_id'])
        if not social_type_exist:
            return CustomeResponse({"msg":"social_type is not there"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        try:
            for key, social_id in social_type.iteritems():
                if key == request.data['social_type_id']:            
                    user_id = request.user
                    social_type_id =  social_id
                    data ={}
                    user_id  = request.user.id
                    datas = createConnectedAccount(user_id,social_type_id)
                    if datas:
                            return CustomeResponse({"msg":"user is connected"},status=status.HTTP_201_CREATED)
                    else:
                        return CustomeResponse({'msg':"user is already connected"},validate_errors=1)
        except:
            user_id = None
            return CustomeResponse({"msg":"social_type_id is not there"},status=status.HTTP_400_BAD_REQUEST,validate_erros=1)
            
        
        
      
    @list_route(methods=['post'],)
    def deleteConnectedAccounts(self,request):
        
        try:
            user_id = request.user
            social_type =  constant.SOCIAL_TYPE
            social_type_exist =social_type.has_key(request.data['social_type_id'])
            if not social_type_exist:
                return CustomeResponse({"msg":"social_type is not there"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        except:
            user_id  = None
            return CustomeResponse({"msg":"social_type_id is mandatory"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        try:
            for key, social_id in social_type.iteritems():
                if key == request.data['social_type_id']:            
                    social_type_id =  social_id
                    sociallogin = SocialLogin.objects.get(user=user_id,social_type=social_type_id)
        except:
            sociallogin =None
            
        if sociallogin is not None:
            return CustomeResponse({"msg":"This account is cannot be deleted because you have sign up with this account"})
        
        connecteddata  =  ConnectedAccount.objects.filter(user_id=user_id,social_type_id=social_type_id)
        if connecteddata:
            connecteddata.delete()
            return CustomeResponse({"msg":"connected account is deleted"})
        else:
            return CustomeResponse({"msg":"There is no connected account for this user"})
        
        
        
       
    
        
        
            
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
    
     #-------------- Work as update user profile -----------------------------#
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
        serializer =  ProfileSerializer(messages,data=request.data,partial=True,context={'request': request})
        if serializer.is_valid():
            serializer.save(first_time_login  = False,profile_image= profile_image)
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
        else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
    
    def partial_update(self, request, pk=None):
        pass

    @list_route(methods=['post'],)
    def deleteprofileimage(self, request, pk=None):
        try:
            user_id = request.user.id
        except:
            user_id = None
        
        profiledata = Profile.objects.get(user_id=user_id)
        profiledata.profile_image.delete()
        if profiledata:
            return CustomeResponse({'msg':'Image is deleted'},status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg':'server error'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    
class SocialLoginViewSet(viewsets.ModelViewSet):     
    queryset = SocialLogin.objects.all()
    serializer_class = SocialLoginSerializer
    
    def create(self, request):
                try:
                  if request.data['status'] is 0:
                     return CustomeResponse({'msg':'provide status active'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
                except:
                  return CustomeResponse({'msg':'provide status active'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   
                serializer =  UserSerializer(data=request.data,context={'request': request,'msg':'not exist'})
                try:               
                 user = checkEmail(request.data['email'])
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
                            # social_type_id for fb its 2---------------#
                            
                            social_type =  constant.SOCIAL_TYPE
                            social_type_exist =social_type.has_key(request.data['social_type'])
                            if  not social_type_exist:
                               return CustomeResponse({'msg':'social_type not exist'}) 
                           
                            for key, social_id in social_type.iteritems():
                                if key == request.data['social_type']:            
                                    social_type_id =  social_id
#                           
                            #social_type = request.POST.get('social_type_id','')
                            sociallogin = SocialLogin(user_id=data['id'],social_media_login_id = social_id,social_type_id=social_type_id)
                            createConnectedAccount(data['id'],social_type_id)
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
    if request.method == 'GET':
       try:
        activation_key = kwargs['activation_key']
       except:
        activation_key = None 
      
       try:
        reset_password_key = kwargs['reset_password_key']
       except:
        reset_password_key = None
       
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
                response = HttpResponse("kinbow://?token="+str(token_value), status=302)
                response['Location'] = "kinbow://?token="+str(token_value)
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
                response = HttpResponse("kinbow://?resetPasswordKey="+reset_password_key, status=302)
                response['Location'] = "kinbow://?resetPasswordKey="+reset_password_key
                return response 
            else:                         
               return CustomeResponse({'msg':'This url is used in app only'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)               
       return CustomeResponse({'msg':'Please provide correct parameters'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)              
    
    if request.method == 'POST':
        try:
          op = request.data['op']
        except:
          op = None  
        # ----------- Login ------------------#
        if op == 'login':
                try:
                    username = request.data['username']
                    password = request.data['password']
                except:
                    username = None
                    password = None
                #------------------- save password in case of forgot passord TODO  move this section from login section----------------#
                try:
                  reset_password_key = request.data['reset_password_key']
                except:
                  reset_password_key = None  
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
                try:                    
                  email = request.data['email']
                except:
                  email = None  
                try:
                 profile = Profile.objects.select_related().get(user__email=request.data['email'],user__user_type__in=[2,3])
                except:
                 profile = ''
                if email:                   
                    
                    if profile and not None:
                        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                        reset_password_key = hashlib.sha1(salt+profile.user.email).hexdigest()
                         
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
                try:
                  email = request.data['email']     
                except:
                  email = None  
                try:
                 profile = Profile.objects.select_related().get(user__email=email)
                except:
                 profile = ''
                
                if profile:
                   user = model_to_dict(profile.user)
                   BaseSendMail.delay(user,type='account_confirmation',key = profile.activation_key)
                   return CustomeResponse({'msg':"email sent"},status=status.HTTP_200_OK)
                else:
                   return CustomeResponse({'msg':"email does not exist"},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1) 
                 
                 
            
        else:
             return CustomeResponse({'msg':'Please provide operation parameter op'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)            


class UserEmailViewSet(viewsets.ModelViewSet):
    queryset = UserEmail.objects.all()
    serializer_class = UserEmailSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get_permissions(self):
        # Your logic should be all here
        if self.request.method == 'GET':
            activation_code = self.request.QUERY_PARAMS.get('activation_code','')
            if activation_code:
                self.authentication_classes = []
                self.permission_classes = []
        else:            
            pass
        return super(viewsets.ModelViewSet, self).get_permissions() 
    def list(self, request):
        default_email = {}
        default_email['email'] = request.user.email
        default_email['is_default'] = 1
        userEmails = self.queryset.filter(user_id=request.user)
        user_id = request.user.id
      
        userEmailSerializer = UserEmailSerializer(userEmails, many=True)
        count = UserEmail.objects.filter(user_id=user_id).count()
        #items= 0
        data = []
#        data.append(userEmailSerializer.data)
#        data.append(default_email)
        i = 0 
        terms ={}
        if userEmailSerializer:
           for items in userEmailSerializer.data:
               if i == 0:
                   data.append(default_email)
                   items['is_default'] = 0
                   data.append(items)
               else:
                   items['is_default'] = 0 
                   data.append(items)
               i = i +1 
        #userEmailSerializer.append(newthing) 
        if userEmailSerializer :
            if count > 0:
                return CustomeResponse(data,status=status.HTTP_200_OK) 
            else:
                data.append(default_email)
                #terms['is_default'] = 1
                #data.append(terms)
                defaultEmail=User.objects.filter(id=user_id)
                serializer = UserSerializer(defaultEmail,many=True)
                return CustomeResponse(data,status=status.HTTP_200_OK)
        else :
            return CustomeResponse(default_email,status=status.HTTP_200_OK)

    def create(self,request):
        try:
            user_id = request.user
        except:
            user_id = None
        data ={}
        data['user_id'] = request.user.id
        data['email'] = request.data.get('email')
        data['is_default'] = 0
        #todo email validation in serializer 
        serializer = UserEmailSerializer(data=data,context ={'request':request,'msg':'not exist'})
        
        if serializer.is_valid():
                serializer.save()
                return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse({'msg':serializer.errors},validate_errors=1)

                 
    @list_route(methods=['post'],)
    def send_verification_code(self,request):
        
        try:
            user_id = request.user
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5] 
            data ={}
            data['email'] = request.data.get('email')
            data['id'] = request.user.id
            
            activation_key = hashlib.sha1(salt+data['email']).hexdigest()[:10] 
            if user_id:
                UserEmail.objects.filter(user_id=request.user.id,email=request.data.get('email')).update(verification_code=activation_key)
                BaseSendMail.delay(data,type='verify_email',key = activation_key)
                return CustomeResponse({'msg':'verification code sent'},status=status.HTTP_200_OK)
            else:
                return CustomeResponse({'msg':'server error'},validate_errors=1)
            
            if not data['email']:
                return CustomeResponse({"msg":"email is not there"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        except:
            data['email']  = None
            return CustomeResponse({"msg":"email is mandatory"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
   
    @list_route(methods=['get'],)
    def verify_email(self,request):

            activation_code = self.request.QUERY_PARAMS.get('activation_code','')
            user_email = UserEmail.objects.select_related('user_id').get(verification_code=activation_code)
            data ={}
            data['ueid']=user_email.id #added user email pk
            userEmail=user_email.user_id.email
            userEmailAdded = user_email.email
            isVerified = user_email.isVerified
     
            try:
                #userEmailAdded = UserEmail.objects.filter(id=data['ueid']).values('isVerified','email')
                checkUserEmail=User.objects.filter(email=userEmailAdded) # check email user table if exist
            except:
                return CustomeResponse({"msg":"email is not there"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    
            if user_email:
                if isVerified==0:
                    #user_email.update(isVerified=1,verification_code='')
                    UserEmail.objects.filter(id=data['ueid']).update(isVerified=1,verification_code='')
                    return CustomeResponse({'msg':'email verified'},status=status.HTTP_200_OK)
                    
                elif isVerified==1:
                    #user_email.update(isVerified=2,verification_code='')
                    UserEmail.objects.filter(id=data['ueid']).update(isVerified=2,verification_code='')
                    #tempUserEmail= userEmailAdded[0]['email'] 
                    if not checkUserEmail: 
                        UserEmail.objects.filter(id=data['ueid']).update(email= userEmail)
                        User.objects.filter(id=request.user.id).update(email=userEmailAdded)    
                        return CustomeResponse({'msg':'email set to default'},status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse({'msg':'email cannot be replaced'},validate_errors=1)
                
                else:
                    return CustomeResponse({'msg':'server error'},validate_errors=1)
            
                if not userEmail:
                    return CustomeResponse({"msg":"email is not there"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                
                elif request.device:
                    from django.http import HttpResponse
                    response = HttpResponse("kinbow://verify_email=1", status=302)
                    response['Location'] = "kinbow://?verify_email=1"
                    return response 
                else:                 
                    return CustomeResponse({'msg':'email verified'},status=status.HTTP_200_OK)
            else:
                return CustomeResponse({'msg':'activation_code does not exist.'},validate_errors=1)              
     
            
    
    @list_route(methods=['post'],)
    def setdefault(self, request):
        
        user_id = request.user
        data ={}
        data['id'] = request.user.id
        data['ueid'] = request.data.get('useremail_id')
        userEmail = request.user.email

        try:
            #set default status(2) of all emails to 1
            UserEmail.objects.filter(user_id=request.user.id,isVerified=2).update(isVerified=1)
            userEmailAdded = UserEmail.objects.filter(id=data['ueid']).values('isVerified','email')
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5] 
            activation_key = hashlib.sha1(salt+userEmailAdded[0]['email']).hexdigest()[:10]
            data['email'] = userEmailAdded[0]['email']
           
            if user_id:
                UserEmail.objects.filter(id=data['ueid']).update(verification_code=activation_key)
                BaseSendMail.delay(data,type='verify_email',key = activation_key)
                return CustomeResponse({'msg':'verification code sent'},status=status.HTTP_200_OK)
            else:
                return CustomeResponse({'msg':'server error'},validate_errors=1)
        
        except:
            return CustomeResponse({"msg":"email is not there"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
  
    
    @list_route(methods=['post'],)
    def deleteEmail(self, request, pk=None):
        try:
            user_id = request.user.id
    
            #userEmailId = self.request.QUERY_PARAMS.get('id')
            userEmailId = request.data['userEmailId']
        except:
            userEmailId = ''
        try:
            #checkEmail=UserEmail.objects.filter(user_id=user_id)
            count = UserEmail.objects.filter(user_id=user_id).count()
            userEmail=UserEmail.objects.filter(id=request.data['userEmailId'])  
        
        except:
            return CustomeResponse({'msg':'Email not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        if count > 0:
            if userEmail:
                userEmail.delete()
                return CustomeResponse({'msg':'Email is deleted'},status=status.HTTP_200_OK)
            
        if count == 0:
            defaultEmail=User.objects.filter(id=user_id)
            serializer = UserSerializer(defaultEmail,many=True)
            return CustomeResponse(data=serializer.data,status=status.HTTP_200_OK)
        
        else:
            return CustomeResponse({'msg':'server error'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        

