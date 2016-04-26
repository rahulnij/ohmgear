
from rest_framework import serializers
from apps.folders.serializer import FolderContactSerializer
from models import Contacts, FavoriteContact, AssociateContact, ContactMedia,PrivateContact
from django.conf import settings


class ContactMediaSerializer(serializers.ModelSerializer):

    img_url = serializers.ImageField(
        max_length=None, use_url=True, required=True)

    class Meta:
        model = ContactMedia
        fields = ('user_id', 'contact_id', 'img_url',
                  'front_back', 'position', 'status')


class ContactsSerializer(serializers.ModelSerializer):

    folder_contact_data = FolderContactSerializer(many=True, read_only=True)
    businesscard_media = ContactMediaSerializer(many=True, read_only=True)

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

#   Used in fetch contact data


class PrivateContactSerializer(serializers.ModelSerializer):

    class Meta(object):
        """Private Contact data"""
        model = PrivateContact


class ContactsSerializerWithJson(serializers.ModelSerializer):

    bcard_json_data = serializers.SerializerMethodField(
        'clean_bcard_json_data')
    folder_contact_data = FolderContactSerializer(many=True, read_only=True)
#    businesscard_media = ContactMediaSerializer(many=True,read_only=True)

    businesscard_media = serializers.SerializerMethodField(
        'bcard_image_frontend')

    def bcard_image_frontend(self, obj):
        media = ContactMedia.objects.filter(
            contact_id=obj.id, status=1).order_by('front_back')
        data = []

        for item in media:
            data.append({"img_url": str(settings.DOMAIN_NAME) +
                         str(settings.MEDIA_URL) +
                         str(item.img_url), "front_back": item.front_back})
        return data

    def clean_bcard_json_data(self, obj):
        return obj.bcard_json_data

    class Meta:
        model = Contacts
        fields = (
            'id',
            'businesscard_id',
            'bcard_json_data',
            'user_id',
            'folder_contact_data',
            'businesscard_media',
            'created_date',
            'updated_date'
        )


class FavoriteContactSerializer(serializers.ModelSerializer):

    folder_contact_data = serializers.ReadOnlyField(
        source='foldercontact_id.contact_id.bcard_json_data')
    contact_id = serializers.ReadOnlyField(
        source='foldercontact_id.contact_id.id')

    businesscard_media = serializers.SerializerMethodField(
        'bcard_image_frontend')

    def bcard_image_frontend(self, obj):
        media = ContactMedia.objects.filter(
            contact_id=obj.id, status=1).order_by('front_back')
        data = []
        for item in media:
            data.append({"img_url": str(settings.DOMAIN_NAME) +
                         str(settings.MEDIA_URL) +
                         str(item.img_url), "front_back": item.front_back})

        return data

    class Meta:
        model = FavoriteContact
        fields = ('user_id', 'foldercontact_id', 'folder_contact_data',
                  'contact_id', 'businesscard_media')


class AssociateContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssociateContact
