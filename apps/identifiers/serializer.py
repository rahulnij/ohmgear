from django.conf.urls import url, include
#from apps.identifiers.models import Identifier
from models import Identifier
from rest_framework import routers, serializers, viewsets
from functions import validate_identifier
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
            
            
class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        fields = ('id','user','identifier','identifiertype','identifierlastdate')
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
                 
            
        return attrs 
            