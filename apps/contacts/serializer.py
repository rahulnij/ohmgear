
from rest_framework import serializers
from apps.folders.serializer import FolderContactSerializer
from models import Contacts, FavoriteContact, AssociateContact, ContactMedia, PrivateContact
from apps.contacts.models import FolderContact
from apps.businesscards.models import BusinessCardAddSkill
from apps.groups.models import GroupContacts
from apps.notes.models import Notes

from django.conf import settings
import rest_framework.status as status
from ohmgear.functions import CustomeResponse
import logging
logger = logging.getLogger(__name__)


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
            'created_date',
            'updated_date',
            'contact_profile_image'
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

    contact_profile_url = serializers.SerializerMethodField('get_thumbnail_url')

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


    def get_thumbnail_url(self, obj):
        if obj.contact_profile_image:
            return '%s' % (str(settings.DOMAIN_NAME) +
                           str(settings.MEDIA_URL) +
                           str(obj.contact_profile_image))

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
            'updated_date',
            'contact_profile_url'
        )


class FavoriteContactSerializer(serializers.ModelSerializer):

    folder_contact_data = serializers.ReadOnlyField(
        source='foldercontact_id.contact_id.bcard_json_data')
    contact_id = serializers.ReadOnlyField(
        source='foldercontact_id.contact_id.id')

    businesscard_media = serializers.SerializerMethodField(
        'bcard_image_frontend')

    def bcard_image_frontend(self, obj):
        foldercontact_data = obj.foldercontact_id
        contact_id = foldercontact_data.contact_id.id
        try:
            media = ContactMedia.objects.filter(
                contact_id=contact_id, status=1).order_by('front_back')
        except ContactMedia.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, contact_id {},\
                    in {}".format(
                    self.__class__, contact_id, __file__
                )
            )
            return CustomeResponse(
                {
                    "msg": "ContactMedia does not exist."
                },
                status=status.HTTP_404_NOT_FOUND,
                validate_errors=1
            )
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


# it is used in user contact list

class FolderContactWithDetailsSerializer(serializers.ModelSerializer):

    contact_data = serializers.ReadOnlyField(
        source='contact_id.bcard_json_data')

    contact_media = serializers.SerializerMethodField(
        'contact_media_funct')

    def contact_media_funct(self, obj):
        media = ContactMedia.objects.filter(
            contact_id=obj.contact_id, status=1).order_by('front_back')
        data = []

        for item in media:
            data.append({"img_url": str(settings.DOMAIN_NAME) +
                         str(settings.MEDIA_URL) +
                         str(item.img_url), "front_back": item.front_back})
        return data
    private_contact_data = PrivateContactSerializer(read_only=True)

    class Meta:
        model = FolderContact
        fields = (
            'id',
            'user_id',
            'folder_id',
            'contact_id',
            'link_status',
            'is_linked',
            'contact_data',
            'contact_media',
            'private_contact_data',
            'created_date',
            'updated_date',
        )


# get the contact details and related data

class FolderContactWithRelatedDataSerializer(serializers.ModelSerializer):

    contact_data = serializers.ReadOnlyField(
        source='contact_id.bcard_json_data')

    related_data = serializers.SerializerMethodField(
        'related_data_funct')

    # get the contact skill, media, history, notes
    def related_data_funct(self, obj):

        # tried to pull data from select related but fail, need to look
        data = {}
        media = ContactMedia.objects.filter(
            contact_id=obj.contact_id, status=1).order_by('front_back')
        data_media = []

        for item in media:
            data_media.append({"img_url": str(settings.DOMAIN_NAME) +
                               str(settings.MEDIA_URL) +
                               str(item.img_url), "front_back": item.front_back})
        if media:
            data['contact_media'] = data_media
        else:
            data['contact_media'] = []

        # skills
        data_skills = []
        skills = BusinessCardAddSkill.objects.filter(
            businesscard_id=obj.contact_id.businesscard_id).values()
        for item in skills:
            data_skills.append(item)

        if skills:
            data['skills'] = data_skills
        else:
            data['skills'] = []

        # history
        data_history = []
        if obj.contact_id.businesscard_id:
            history = obj.contact_id.history.filter(
                businesscard_id=obj.contact_id.businesscard_id).order_by('-id')[:5].values()
            for item in history:
                data_history.append(item)
            data['history'] = data_history
        else:
            data['history'] = []

        # groups
        data_groups = []
        groups = GroupContacts.objects.filter(
            folder_contact_id=obj.id)
        for item in groups:
            data_groups.append({"id": item.id,
                                "group_id": item.group_id.id,
                                "group_name": item.group_id.group_name,
                                "folder_contact_id": item.folder_contact_id.id,
                                "created_date": item.created_date,
                                "updated_date": item.updated_date
                                })

        if groups:
            data['groups'] = data_groups
        else:
            data['groups'] = []

        # notes

        data_notes = []
        notes = Notes.objects.filter(
            contact_id=obj.contact_id,
            bcard_side_no__in=[
                1,
                2]).values(
            "id",
            "note",
            "bcard_side_no",
            "contact_id")
        for item in notes:
            data_notes.append(item)

        if notes:
            data['notes'] = data_notes
        else:
            data['notes'] = []

        return data

    private_contact_data = PrivateContactSerializer(read_only=True)

    class Meta:
        model = FolderContact
        fields = (
            'id',
            'user_id',
            'folder_id',
            'contact_id',
            'link_status',
            'is_linked',
            'contact_data',
            'related_data',
            'private_contact_data',
            'created_date',
            'updated_date',
        )
