from django.conf.urls import url, include
from models import UserSetting, Setting, Language, DisplayContactNameAs
from rest_framework import routers, serializers, viewsets


class UserSignupSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSetting


class SettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setting


class UserSettingSerializer(serializers.ModelSerializer):
    #setting_data = SettingSerializer(read_only=True)
    key = serializers.ReadOnlyField(source='setting_id.key')

    class Meta:
        model = UserSetting
        fields = ('value', 'key')


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language


class DisplayContactNameAsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisplayContactNameAs
