from django.conf.urls import url, include
from apps.users.models import User,Profile,SocialLogin,ConnectedAccount,UserEmail,SocialType
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False,allow_blank=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=get_user_model().objects.all(),message='Email id is already registered with ohmgear')])
    class Meta:
        model = get_user_model()
        fields = ('id','account_number','email','email_verification_code','user_type','pin_number','status','password')
#        read_only_fields = ('id',)

    def validate_user_type(self, attrs):
        value = attrs
        if value.id == 1:
            raise serializers.ValidationError("user_type must be individual")
        elif value.id == 2:
            pass
        else: 
            print "other"
            raise serializers.ValidationError("user_type must be individual")
            
            
        return attrs 
       
class ProfileSerializer(serializers.ModelSerializer):
    #profile_image = serializers.ImageField(max_length=None, use_url=True,required=False)
    pin_number = serializers.ReadOnlyField(source='user.pin_number')
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Profile

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        # Instantiate the superclass normally
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        
class SocialLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLogin
        
class ConnectedAccountsSerializer(serializers.ModelSerializer):
    social_type = serializers.ReadOnlyField(source='social_type_id.social_type')
    class Meta:
        model   =   ConnectedAccount
        fields = ('user_id','social_type_id','social_type')
        
class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model   =   UserEmail
        
        
        
class SocialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model   =   SocialType