from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from serializer import UserSettingSerializer, SettingSerializer, LanguageSerializer, DisplayContactNameAsSerializer
from models import Setting, UserSetting, Language, DisplayContactNameAs
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from functions import get_all_usersetting, get_setting_value_by_key, update_user_setting
from apps.users.models import User
import re

# Create your views here.


class UserSettingViewSet(viewsets.ModelViewSet):
    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    #---------------------Get all user-setting of a user-----------#
    def list(self, request):
        user_id = request.user.id
        queryset = get_all_usersetting(user_id)
        if queryset:
            serializer = UserSettingSerializer(queryset, many=True)
            data = {keydata['key']: keydata['value'] for keydata in serializer.data}
            return CustomeResponse(data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg": "data not found"}, status=status.HTTP_200_OK)

    @list_route(methods=["post"],)
    #-----------------get particular setting value of user by key--------#
    def getsettingvalue(self, request):
        try:
            getkey = request.data['key']
            user_id = request.user.id
        except:
            return CustomeResponse({"msg": "Please provide the key"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        try:
            usersettingvalue = get_setting_value_by_key(getkey, user_id)

        except:
            return CustomeResponse({"msg": "Key not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        if usersettingvalue:
            serializer = UserSettingSerializer(usersettingvalue)
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    @list_route(methods=["post"],)
    #----------------update settings of the user by key---------#
    def updatekeyvalue(self, request):

        try:
            getkey = request.DATA['key']
            getvalue = request.DATA['value']
            user_id = request.user.id
            getkeydata = update_user_setting(getkey, getvalue, user_id)

        except:
            return CustomeResponse({"msg": "Data not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        if getkeydata:
            return CustomeResponse({"msg": "settings has been updated"}, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg": "Server error try again"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    @list_route(methods=['post'],)
    def update_pinnumber(self, request):
        try:
            user_id = request.user.id
        except:
            user_id = ''

        try:
            pin_number = request.DATA['pin_number']

            if re.match(r'^[0-9]{4}$', pin_number):
                pass
            else:
                return CustomeResponse({"msg": "Pin number can be numeric with 4 digits only "}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        except:
            pin_number = ''

        try:
            userdata = User.objects.filter(
                id=user_id).update(pin_number=pin_number)
        except:
            userdata = None

        if userdata:
            return CustomeResponse({'msg': 'Pin number is updated'}, status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse({"msg": "Server error try again"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)


class LanguageSettingViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_list = LanguageSerializer
    #-------------get all data of language from refrence table

    def list(self, request):
        queryset = Language.objects.all()
        if self.queryset:
            serializer = LanguageSerializer(queryset, many=True)
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg": "Data not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)


class DisplayContactNameAsViewSet(viewsets.ModelViewSet):
    queryset = DisplayContactNameAs.objects.all()
    serializer_list = DisplayContactNameAsSerializer
    #-------------get all data of language from refrence table----------#

    def list(self, request):
        #queryset    =   Language.objects.all()
        queryset = DisplayContactNameAs.objects.all()
        print queryset
        if queryset:
            serializer = DisplayContactNameAsSerializer(queryset, many=True)
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg": "Data not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
