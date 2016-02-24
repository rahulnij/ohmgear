from rest_framework import serializers
from apps.folders.serializer import FolderContactSerializer
from models import Contacts
# Serializers define the API representation.
class ContactsSerializer(serializers.ModelSerializer):
    #bcard_json_data = serializers.CharField()
    #contact_id = serializers.ReadOnlyField(source='contact_id.id')
    folder_contact_data = FolderContactSerializer(many=True,read_only=True)
    class Meta:
        model = Contacts
        fields = (
            'id',
            'businesscard_id',
            'bcard_json_data',
            'user_id',
            'folder_contact_data',
        )

#------------- Used in fetch contact data -------------------#        
class ContactsSerializerWithJson(serializers.ModelSerializer):
    #bcard_json_data = serializers.CharField()
    bcard_json_data = serializers.SerializerMethodField('clean_bcard_json_data')
    def clean_bcard_json_data(self, obj):
        return obj.bcard_json_data    
    
    class Meta:
        model = Contacts
        fields = (
            'id',
            'businesscard_id',
            'bcard_json_data',
            'user_id'
        )        
        