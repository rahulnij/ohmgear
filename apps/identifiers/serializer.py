from django.conf.urls import url, include
#from apps.identifiers.models import Identifier
from models import Identifier,LockIdentifier
from rest_framework import routers, serializers, viewsets
from functions import validate_identifier
from ohmgear.functions import CustomeResponse
import rest_framework.status as status

from apps.businesscards.serializer import BusinessCardSerializer            
            
class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        fields = ('id','user','identifier','identifiertype','paymentstatus','identifierlastdate')


class BusinessIdentifierSerializer(serializers.ModelSerializer):
    business_identifier = BusinessCardSerializer(many=True,read_only=True)
    class Meta:
        model = Identifier
        fields = ('id','user','identifier','identifiertype','paymentstatus','identifierlastdate','business_identifier')


#        read_only_fields = ('id',)

    def validate(self, attrs):
        msg = {}
        value = attrs
        identifier =  value ['identifier'] 
        identifiertype = value['identifiertype']
        
        if identifiertype == 2:
            identifier = validate_identifier(identifier)
            
            if identifier == 0 :
                raise serializers.ValidationError("Identifier is not in correct format")
            
            
        elif identifiertype  == 1:
            pass
            
        else :
            raise serializers.ValidationError("identifiertype can be 1 or 2 only ")
                 
        return attrs 
            
            
            
class LockIdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockIdentifier
            