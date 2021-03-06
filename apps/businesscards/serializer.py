from rest_framework import serializers
from django.conf import settings

from models import BusinessCard, BusinessCardIdentifier, BusinessCardSkillAvailable, BusinessCardAddSkill
from apps.contacts.serializer import ContactsSerializerWithJson
from apps.folders.models import FolderContact
from apps.contacts.models import ContactMedia
from apps.notes.models import Notes

# Serializers define the API representation.


class BusinessCardAddSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessCardAddSkill
        #fields = ('skill_name','businesscard_id',)


class BusinessCardAddSkillSerializerReference(serializers.ModelSerializer):

    class Meta:
        model = BusinessCardAddSkill
        fields = ('skill_name',)

# class BusinessCardMediaSerializer(serializers.ModelSerializer):
#
#    img_url = serializers.ImageField(max_length=None, use_url=True,required=True)
#    class Meta:
#        model = BusinessCardMedia
#        fields = ('user_id','businesscard_id','img_url','front_back','position','status')


class BusinessCardSkillAvailableSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessCardSkillAvailable
        fields = ('skill_name',)


# ----------------- Main Business Card ----------------------------#


class BusinessCardSerializer(serializers.ModelSerializer):

    contact_detail = ContactsSerializerWithJson(read_only=True)

    media_detail = serializers.SerializerMethodField('bcard_image_frontend')
    business_notes = serializers.SerializerMethodField('fetch_notes')

    def bcard_image_frontend(self, obj):
        media = ContactMedia.objects.filter(
            contact_id=obj.contact_detail.id, status=1).order_by('front_back')
        data = []
        for item in media:
            data.append({"img_url": str(settings.DOMAIN_NAME) +
                         str(settings.MEDIA_URL) +
                         str(item.img_url), "front_back": item.front_back})
        return data

    def fetch_notes(self, obj):
        notes = Notes.objects.filter(contact_id=obj.contact_detail.id)
        data = {}
        for item in notes:
            if item.bcard_side_no == 1:
                data['note_frontend'] = str(item.note)
            elif item.bcard_side_no == 2:
                data['note_backend'] = str(item.note)
        return data

    class Meta:
        model = BusinessCard
        fields = (
            'id',
            'name',
            'bcard_type',
            'is_active',
            'status',
            'user_id',
            'contact_detail',
            'media_detail',
            'business_notes',
            'is_default',
            'card_logo',
            'card_logo_backside'
        )

# --------------- Business card serializer wit Identifier : reason : circular error in identifier error --#
from apps.identifiers.serializer import IdentifierSerializer


class BusinessCardWithIdentifierSerializer(serializers.ModelSerializer):

    contact_detail = ContactsSerializerWithJson(read_only=True)
    media_detail = serializers.SerializerMethodField('bcard_image_frontend')
    business_identifier = IdentifierSerializer(many=True, read_only=True)
    business_notes = serializers.SerializerMethodField('fetch_notes')
    card_logo = serializers.SerializerMethodField('get_bcard_logo_url')
    card_logo_backside = serializers.SerializerMethodField('get_bcard_logo_backend_url')

    def bcard_image_frontend(self, obj):
        media = ContactMedia.objects.filter(
            contact_id=obj.contact_detail.id, status=1).order_by('front_back')
        data = []
        for item in media:
            data.append({"img_url": str(settings.DOMAIN_NAME) +
                         str(settings.MEDIA_URL) +
                         str(item.img_url), "front_back": item.front_back})
        return data

    def fetch_notes(self, obj):
        notes = Notes.objects.filter(contact_id=obj.contact_detail.id)
        data = {}
        for item in notes:
            if item.bcard_side_no == 1:
                data['note_frontend'] = str(item.note)
            elif item.bcard_side_no == 2:
                data['note_backend'] = str(item.note)
        return data

    def get_bcard_logo_url(self, obj):
        if obj.card_logo:
            return '%s' % (str(settings.DOMAIN_NAME) +
                           str(settings.MEDIA_URL) +
                           str(obj.card_logo))

    def get_bcard_logo_backend_url(self, obj):
        if obj.card_logo_backside:
            return '%s' % (str(settings.DOMAIN_NAME) +
                           str(settings.MEDIA_URL) +
                           str(obj.card_logo_backside))


    class Meta:
        model = BusinessCard
        fields = (
            'id',
            'name',
            'bcard_type',
            'is_active',
            'status',
            'user_id',
            'contact_detail',
            'media_detail',
            'business_identifier',
            'business_notes',
            'card_logo',
            'card_logo_backside',
            'is_default',
        )


class SearchBusinessCardWithIdentifierSerializer(serializers.ModelSerializer):
    """search by email or name."""

    contact_detail = ContactsSerializerWithJson(read_only=True)
    media_detail = serializers.SerializerMethodField('bcard_image_frontend')
    business_identifier = IdentifierSerializer(many=True, read_only=True)
    business_notes = serializers.SerializerMethodField('fetch_notes')
    search_by = serializers.SerializerMethodField('searchby')

    def searchby(self, obj):
        """It give whether search result is from email or from name."""
        data = self.context['search']
        return data

    def bcard_image_frontend(self, obj):
        """Fetched business card images."""
        media = ContactMedia.objects.filter(
            contact_id=obj.contact_detail.id, status=1).order_by('front_back')
        data = []
        for item in media:
            data.append({"img_url": str(settings.DOMAIN_NAME) +
                         str(settings.MEDIA_URL) +
                         str(item.img_url), "front_back": item.front_back})
        return data

    def fetch_notes(self, obj):
        """Fetch notes of Businesscards."""
        notes = Notes.objects.filter(contact_id=obj.contact_detail.id)
        data = {}
        for item in notes:
            if item.bcard_side_no == 1:
                data['note_frontend'] = str(item.note)
            elif item.bcard_side_no == 2:
                data['note_backend'] = str(item.note)
        return data

    class Meta:
        """Required filds."""

        model = BusinessCard
        fields = (
            'id',
            'name',
            'bcard_type',
            'is_active',
            'status',
            'user_id',
            'contact_detail',
            'media_detail',
            'business_identifier',
            'business_notes',
            'search_by'
        )


from apps.vacationcard.serializer import VacationCardSerializer


class BusinessCardSummarySerializer(serializers.HyperlinkedModelSerializer):
    businesscard_skills = BusinessCardAddSkillSerializerReference(
        many=True, read_only=True)
    business_identifier = IdentifierSerializer(many=True, read_only=True)
    business_vacation = VacationCardSerializer(many=True, read_only=True)
    contact_detail = ContactsSerializerWithJson(read_only=True)
    business_media = serializers.SerializerMethodField('bcard_image_frontend')

    def bcard_image_frontend(self, obj):
        media = ContactMedia.objects.filter(
            contact_id=obj.contact_detail.id, status=1).order_by('front_back')
        data = []
        for item in media:
            data.append({"img_url": str(settings.DOMAIN_NAME) +
                         str(settings.MEDIA_URL) +
                         str(item.img_url), "front_back": item.front_back})
        return data
    # ------------------------ End -------------- #

    class Meta:
        model = BusinessCard
        fields = (
            'id',
            'name',
            'businesscard_skills',
            'business_identifier',
            'business_vacation',
            'contact_detail',
            'business_media',
        )


class BusinessCardIdentifierSerializer(serializers.ModelSerializer):

    bcard_detail = serializers.SerializerMethodField('bcard_data')

    def bcard_data(self, instance):
        return instance.bcard_data()

    class Meta:
        model = BusinessCardIdentifier
        fields = ('id', 'identifier_id', 'businesscard_id',
                  'status', 'bcard_detail')

    def validate(self, attrs):

        value = attrs
        businesscardid = value['businesscard_id']
        businesscardid = businesscardid.id

        businesscardidentifierdata = BusinessCardIdentifier.objects.filter(
            businesscard_id=businesscardid)
        if not businesscardidentifierdata:
            pass
        else:
            totalbusinesscardrecord = businesscardidentifierdata.count()

            for i in range(totalbusinesscardrecord):
                identifierstatus = businesscardidentifierdata[i].status
                if(identifierstatus == 1):
                    raise serializers.ValidationError(
                        "Businesscard can have 1 identifier only")

        return attrs


class CountContactInBusinesscardSerializer(serializers.ModelSerializer):
    """
    How many contacts businesscard contains

    Also contact_detail of contacts
    """
    folder_contact_detail = serializers.SerializerMethodField('folder_contact')

    def folder_contact(self, obj):
        user = self.context.get("request")
        user_id = user
        folder = FolderContact.objects.select_related('folder_id').filter(
            folder_id__businesscard_id=obj.id, user_id=user_id).values()
        print folder
        return {"data": folder, "count": folder.count()}

    class Meta:
        model = BusinessCard
        fields = (
            'id',
            'name',
            'is_active',
            'status',
            'user_id',
            'folder_contact_detail',
        )


from apps.vacationcard.serializer import VacationTripSerializer
from apps.vacationcard.models import VacationCard

class SingleVacationCardSerializer(serializers.ModelSerializer):

    business_vacation = BusinessCardSerializer(many=True, read_only=True)
    vacation_trips = VacationTripSerializer(many=True, read_only=True)

    class Meta:
        model = VacationCard
        fields = ('id', 'user_id', 'vacation_name',
                  'vacation_trips', 'business_vacation')
