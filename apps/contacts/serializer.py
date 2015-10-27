from rest_framework import serializers

from models import Contacts
# Serializers define the API representation.
class ContactsSerializer(serializers.ModelSerializer):
    #bcard_json_data = serializers.CharField()
    class Meta:
        model = Contacts
        fields = (
            'id',
            'businesscard_id',
            'bcard_json_data',
            'template_id',
            'user_id'
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
            'template_id',
            'user_id'
        )        
        