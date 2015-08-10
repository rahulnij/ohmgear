from django.conf.urls import url, include
from apps.users.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from django.contrib.auth import profile_model
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
#        fields = ('id','account_number','first_name','last_name','email','emai_verification_code','user_type','pin_number','status',)
#        read_only_fields = ('id',) 

    def create(self, validated_data):

        user = get_user_model().objects.create(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
        
 class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = profile_model()
#        fields = ('id','dob','address','mobile_number','user_id','custom_data','income_group','business_type','status',)
#        read_only_fields = ('id',) 

    def create(self, validated_data):

        profile = profile_model().objects.create(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user       
