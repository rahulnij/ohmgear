from django.shortcuts import render
from rest_framework import routers,serializers,viewsets
from serializer import UserSettingSerializer,SettingSerializer,LanguageSerializer,DisplayContactNameAsSerializer
from models import Setting,UserSetting,Language,DisplayContactNameAs
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route


# Create your views here.
class UserSettingViewSet(viewsets.ModelViewSet):
    queryset = UserSetting.objects.all() 
    serializer_class = UserSettingSerializer
    authentication_classes  = (ExpiringTokenAuthentication,)
    permission_classes      =  (IsAuthenticated,)
    
    #---------------------Get all user-setting of a user-----------#
    def list(self,request):
        user_id =request.user.id
        queryset  = UserSetting.objects.filter(user_id=user_id)
        serializer = UserSettingSerializer(queryset, many=True)                        
        data= { keydata['key']:keydata['value'] for keydata in serializer.data}
        return CustomeResponse(data,status=status.HTTP_200_OK)
    
    @list_route(methods=["post"],)
    #-----------------get particular setting value of user by key--------#
    def getsettingvalue(self,request):
        try:
            getkey =    request.DATA['key']
        except:
            return CustomeResponse({"msg":"Key not found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        usersettingvalue = UserSetting.objects.get(setting_id__key=getkey,user_id=request.user.id)
        if usersettingvalue:
            serializer      =   UserSettingSerializer(usersettingvalue)
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
        else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    
    
    @list_route(methods=["post"],)
    #----------------update settings of the user by key---------#
    def updatekeyvalue(self,request):

        try:
            getkey      =   request.DATA['key']
            getvalue       =   request.DATA['value']
            getkeydata  =   UserSetting.objects.filter(setting_id__key=getkey,user_id=request.user.id).update(value=getvalue)
            
        except:
            return CustomeResponse({"msg":"Data not found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        if getkeydata:
            return CustomeResponse({"msg":"settings has been updated"},status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg":"Server error try again"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
class LanguageSettingViewSet(viewsets.ModelViewSet):
    queryset    =   Language.objects.all()
    serializer_list =   LanguageSerializer
    #-------------get all data of language from refrence table
    def list(self,request):
        queryset    =   Language.objects.all()
        if self.queryset:
            serializer =    LanguageSerializer(queryset,many=True)
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg":"Data not found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
class DisplayContactNameAsViewSet(viewsets.ModelViewSet):
    queryset    =   DisplayContactNameAs.objects.all()
    serializer_list =   DisplayContactNameAsSerializer
    #-------------get all data of language from refrence table----------#
    def list(self,request):
        #queryset    =   Language.objects.all()
        queryset    =   DisplayContactNameAs.objects.all()
        print queryset
        if queryset:
            serializer =    DisplayContactNameAsSerializer(queryset,many=True)
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg":"Data not found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    
            
        
        
        
         
         
    
    
