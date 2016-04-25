import logging
import json
from rest_framework import serializers

from models import SendRequest
from apps.contacts.models import Contacts
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
                get_contact_data = Contacts.objects.get(
                    id=obj. sender_business_card_id.contact_detail.id)
            except Contacts.DoesNotExist as e:
                logger.error(
                    "Object DoesNotExist: Contacts: {}, {}".format(
                        obj.id, e))
                return data
        else:
            return data

        data['id'] = get_contact_data.id
        data['bcard_json_data'] = get_contact_data.bcard_json_data
        return data

    def receiver_data_func(self, obj):
        data = {}
        filter_type = self.context.get("filter_type")
        if filter_type is not 'received':
            try:
                get_contact_data = Contacts.objects.get(
                    id=obj.sender_business_card_id.contact_detail.id)
            except Contacts.DoesNotExist as e:
                logger.error(
                    "Object DoesNotExist: Contacts: {}, {}".format(
                        obj.id, e))
                return data
        else:
            return data

        data['id'] = get_contact_data.id
        data['bcard_json_data'] = get_contact_data.bcard_json_data
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
            'request_status',
            'sender_data',
            'receiver_data',
        )
