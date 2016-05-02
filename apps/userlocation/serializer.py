# Third Party Imports
from rest_framework import serializers
from django.db.models import Q
import logging

# Local app imports
from models import UserLocation
from apps.users.serializer import ProfileSerializer
from apps.usersetting.models import (
    Setting,
    UserSetting
)
from apps.sendrequest.models import SendRequest

logger = logging.getLogger(__name__)


class UserLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLocation


class ProfileWithConnectionStatusSerializer(
        ProfileSerializer, serializers.ModelSerializer):

    defaultbusinesscard_id = serializers.SerializerMethodField(
        'default_businesscard'
    )
    is_connected = serializers.SerializerMethodField(
        'isconnected'
    )

    class Meta(ProfileSerializer.Meta):
        pass

    def default_businesscard(self, profile_serializer):
        try:
            # todo: find way to do this with join.
            # find setting id for DEFAULT_BUSINESS_CARD setting
            setting = Setting.objects.get(key='DEFAULT_BUSINESS_CARD')

            usersetting = UserSetting.objects.get(
                user_id=profile_serializer.user_id,
                setting_id=setting.id
            )
            return usersetting.value

        except Setting.DoesNotExist:
            logger.critical(
                "Caught DoesNotExist exception for {} in {}".format(
                    Setting.__name__, __file__
                ), exc_info=True
            )
        except Setting.MultipleObjectsReturned:
            logger.critical(
                "Caught MultipleObjectsReturned exception for {}\
                 in {}".format(
                    Setting.__name__, __file__
                ),
                exc_info=True
            )
        except UserSetting.DoesNotExist:
            logger.critical(
                "Caught DoesNotExist exception for {} in {}".format(
                    UserSetting.__name__, __file__
                ),
                exc_info=True
            )
        except UserSetting.MultipleObjectsReturned:
            logger.critical(
                "Caught MultipleObjectsReturned exception for {}\
                 in {}".format(
                    UserSetting.__name__, __file__
                ),
                exc_info=True
            )
        return 0

    def isconnected(self, obj):
        connected_user_id = self.context.get('connected_user_id')
        CONNECTED = 1
        NOT_CONNECTED = 0
        try:
            """get last request AcceptedStatus"""
            send_request = SendRequest.objects.order_by('-updated_date').get(
                sender_user_id=connected_user_id,
                receiver_user_id=obj.user_id
            )

            if send_request.request_status is CONNECTED:
                return CONNECTED

        except SendRequest.DoesNotExist:
            """Not find reason for logging here. it is just to find user\
             connected or not"""
        return NOT_CONNECTED
