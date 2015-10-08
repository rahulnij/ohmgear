from rest_framework import  serializers
from models import BusinessCard
from apps.contacts.serializer import ContactsSerializerWithJson
# Serializers define the API representation.
class BusinessCardSerializer(serializers.ModelSerializer):
    
    #contact_detail = serializers.RelatedField(read_only= True)
    #contact_detail1 = serializers.RelatedField(source='contact_detail',read_only= True)
    contact_detail = ContactsSerializerWithJson(read_only=True)
    class Meta:
        model = BusinessCard
        fields = (
            'id',
            'name',
            'bcard_type',
            'status',
            'is_Active',
            'user',
            'contact_detail'
        )
        
        
        