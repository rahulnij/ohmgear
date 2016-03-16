from rest_framework import serializers
from apps.folders.serializer import FolderContactSerializer
from models import Contacts,FavoriteContact,AssociateContact,ContactMedia
# Serializers define the API representation.


class ContactMediaSerializer(serializers.ModelSerializer):
    
    img_url = serializers.ImageField(max_length=None, use_url=True,required=True)
    class Meta:
        model = ContactMedia
        fields = ('user_id','contact_id','img_url','front_back','position','status')
        

class ContactsSerializer(serializers.ModelSerializer):
    #bcard_json_data = serializers.CharField()
    #contact_id = serializers.ReadOnlyField(source='contact_id.id')
    folder_contact_data = FolderContactSerializer(many=True,read_only=True)
    businesscard_media = ContactMediaSerializer(many=True,read_only=True)
    class Meta:
        model = Contacts
        fields = (
            'id',
            'businesscard_id',
            'bcard_json_data',
            'user_id',
            'folder_contact_data',
            'businesscard_media',
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
        

        
        
class FavoriteContactSerializer(serializers.ModelSerializer):
    
     folder_contact_data = serializers.ReadOnlyField(source='foldercontact_id.contact_id.bcard_json_data')
     contact_id = serializers.ReadOnlyField(source='foldercontact_id.contact_id.id')
     class Meta:
        model = FavoriteContact
        fields = ('user_id','foldercontact_id','folder_contact_data','contact_id')
        
        
class AssociateContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociateContact
        
        
        