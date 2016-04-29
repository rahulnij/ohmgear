# Third Party Imports
from rest_framework import serializers
import logging

# Local app imports
from models import UserLocation
from apps.users.serializer import ProfileSerializer
from apps.usersetting.models import (
    Setting,
    UserSetting
)

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
        return 0
