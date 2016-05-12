import logging
import json
from rest_framework import serializers

from models import SendRequest
from apps.contacts.models import Contacts
from apps.businesscards.models import BusinessCard

from apps.contacts.functions import get_contact_media
# Serializers define the API representation.

logger = logging.getLogger(__name__)


class SendRequestSerializer(serializers.ModelSerializer):

    sender_data = serializers.SerializerMethodField('sender_data_func')
    receiver_data = serializers.SerializerMethodField('receiver_data_func')

    def sender_data_func(self, obj):
        data = {}
        filter_type = self.context.get("filter_type")
        if filter_type is not 'sent':
            try:
                get_contact_data = obj.sender_business_card_id.contact_detail
            except Contacts.DoesNotExist as e:
                logger.error(
                    "Object DoesNotExist: Contacts: {}, {}".format(
                        obj.id, e))
                return data
        else:
            return data

        data['id'] = get_contact_data.id
        data['bcard_json_data'] = get_contact_data.bcard_json_data
        data['contact_media'] = get_contact_media(
            obj.sender_business_card_id.contact_detail.businesscard_media.all())
        return data

    def receiver_data_func(self, obj):
        data = {}
        filter_type = self.context.get("filter_type")
        if filter_type is not 'received':
            try:
                if obj.request_type == 'b2b':
                    try:
                        business_card = BusinessCard.objects.get(
                            id=obj.receiver_bcard_or_contact_id)
                    except BusinessCard.DoesNotExist as e:
                        logger.error(
                            "Object DoesNotExist: Contacts: {}, {}".format(
                                obj.receiver_bcard_or_contact_id.id, e))
                        return data
                    contact_id = business_card.contact_detail.id
                else:
                    contact_id = obj.receiver_bcard_or_contact_id

                get_contact_data = Contacts.objects.get(
                    id=contact_id)
            except Contacts.DoesNotExist as e:
                logger.error(
                    "Object DoesNotExist: Contacts: {}, {}".format(
                        obj.id, e))
                return data
        else:
            return data
        data['id'] = get_contact_data.id
        data['bcard_json_data'] = get_contact_data.bcard_json_data
        data['contact_media'] = get_contact_media(
            get_contact_data.businesscard_media.all())
        return data

    class Meta:
        model = SendRequest
        fields = (
            'id',
            'request_type',
            'sender_user_id',
            'sender_business_card_id',
            'receiver_user_id',
            'receiver_bcard_or_contact_id',
            'message',
            'search_by',
            'request_status',
            'sender_data',
            'receiver_data',
            'created_date',
            'updated_date',
        )
