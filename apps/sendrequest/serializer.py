from rest_framework import serializers

from models import SendRequest
from apps.businesscards.models import BusinessCard
# Serializers define the API representation.


class SendRequestSerializer(serializers.ModelSerializer):
    
    sender_data1 = serializers.SerializerMethodField('sender_data_func')
    receiver_data1 = serializers.SerializerMethodField('receiver_data_func')

    def sender_data_func(self, obj):
        #notes = BusinessCard.objects.get(contact_id=obj.contact_detail.id)
        data = {}
        return data

    def receiver_data_func(self, obj):
        data = {}
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
            'sender_data1',
            'receiver_data1',
        )
