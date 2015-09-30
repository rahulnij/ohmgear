from rest_framework import serializers

from models import Contact
# Serializers define the API representation.
class ContactsSerializer(serializers.ModelSerializer):
    #bcard_json_data = serializers.CharField()
    bcard_json_data = serializers.SerializerMethodField('clean_bcard_json_data')
    def clean_bcard_json_data(self, obj):
        return obj.bcard_json_data    
    
    class Meta:
        model = Contact
        fields = (
            'id',
            'businesscard',
            'bcard_json_data',
            'template',
        )
        