"""Usersetting view."""
from rest_framework import viewsets
from django.conf import settings
import logging

from serializer import (
    UserSettingSerializer,
    LanguageSerializer,
    DisplayContactNameAsSerializer
)

from models import (
    UserSetting,
    Language,
    DisplayContactNameAs
)
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from functions import (
    get_all_usersetting,
    get_setting_value_by_key,
    update_user_setting
)
from apps.users.models import User
import re

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)


class UserSettingViewSet(viewsets.ModelViewSet):
    """Usersetting view."""

    queryset = UserSetting.objects.all()
    serializer_class = UserSettingSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # Get all user-setting of a user
    def list(self, request):
        """Get default user-setting."""
        try:
            user_id = request.user.id
            queryset = get_all_usersetting(user_id)
            if queryset:
                serializer = UserSettingSerializer(queryset, many=True)
                data = {keydata['key']: keydata['value'] for keydata in serializer.data}
                return CustomeResponse(data, status=status.HTTP_200_OK)
            else:
                return CustomeResponse(
                    {"msg": "data not found"}, status=status.HTTP_200_OK)
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=["post"],)
    # get particular setting value of user by key#
    def getsettingvalue(self, request):
        """Get user default setting value by key."""
        try:
            getkey = request.data['key']
            user_id = request.user.id
        except KeyError:
            return CustomeResponse(
                {
                    "msg": "Please provide the key"
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        try:
            usersettingvalue = get_setting_value_by_key(getkey, user_id)

            serializer = UserSettingSerializer(usersettingvalue)
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        except UserSetting.DoesNotExist:
            return CustomeResponse(
                {
                    "msg": "Key not found"
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=["post"],)
    # Update settings of the user by key#
    def updatekeyvalue(self, request):
        """Update setting value by key."""
        try:
            getkey = request.data['key']
            getvalue = request.data['value']
            user_id = request.user.id
            getkeydata = update_user_setting(getkey, getvalue, user_id)

            if getkeydata:
                return CustomeResponse(
                    {"msg": "settings has been updated"},
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {"msg": "Setting Not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def update_pinnumber(self, request):
        """Update pin number."""
        user_id = request.user.id
        try:
            pin_number = request.data['pin_number']

            if re.match(r'^[0-9]{4}$', pin_number):
                pass
            else:
                return CustomeResponse(
                    {
                        "msg": "Pin number can be numeric with 4 digits only "
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except KeyError:
            pin_number = ''

        try:
            User.objects.get(
                id=user_id
            ).update(
                pin_number=pin_number
            )
            return CustomeResponse(
                {'msg': 'Pin number is updated'},
                status=status.HTTP_201_CREATED
            )
        except User.DoesNotExist:
            return CustomeResponse(
                {"msg": "User not exist."},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )


class LanguageSettingViewSet(viewsets.ModelViewSet):
    """Language view."""

    queryset = Language.objects.all()
    serializer_list = LanguageSerializer
    # get all data of language from refrence table#

    def list(self, request):
        """Get all language."""
        try:
            queryset = self.queryset
            if queryset:
                serializer = LanguageSerializer(queryset, many=True)
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {"msg": "Data not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )


class DisplayContactNameAsViewSet(viewsets.ModelViewSet):
    """DisplayContactName View."""

    queryset = DisplayContactNameAs.objects.all()
    serializer_list = DisplayContactNameAsSerializer
    # get all data of language from refrence table

    def list(self, request):
        """Get all DisplayContactName data."""
        try:
            queryset = self.queryset
            if queryset:
                serializer = DisplayContactNameAsSerializer(queryset, many=True)
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {"msg": "Data not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )
