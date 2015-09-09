from django.conf.urls import url, include
from apps.users.models import User,Profile,SocialLogin
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False,allow_blank=True)
    class Meta:
        model = get_user_model()
        fields = ('id','account_number','first_name','last_name','email','email_verification_code','user_type','pin_number','status','password')
#        read_only_fields = ('id',)

    def validate_user_type(self, attrs):
        value = attrs
        if value.id == 1:
            print '1'
            raise serializers.ValidationError("user_type must be individual")
        elif value.id == 2:
            print "2"
        else: 
            print "other"
            raise serializers.ValidationError("user_type must be individual")
            
            
        return attrs 
       
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        
class SocialLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLogin