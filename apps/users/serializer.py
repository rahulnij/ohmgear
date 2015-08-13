from django.conf.urls import url, include
from apps.users.models import User,Profile,SocialLogin
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True,required=False,allow_blank=True)
    class Meta:
        model = get_user_model()
        fields = ('id','account_number','first_name','last_name','email','emai_verification_code','user_type','pin_number','status','password')
#        read_only_fields = ('id',) 
       
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        
class SocialLoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialLogin