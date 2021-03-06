"""Offline views."""

# Third Party Imports
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from django.conf import settings
import rest_framework.status as status
import logging

# Application imports
from apps.businesscards.views import (
    BusinessViewSet,
    BusinessCardIdentifierViewSet
)
from apps.vacationcard.views import VacationCardViewSet
from apps.businesscards.models import BusinessCard
from apps.usersetting.models import UserSetting
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)


class OfflineSendReceiveDataViewSet(viewsets.ModelViewSet):
    """offline views."""

    queryset = BusinessCard.objects.none()
    serializer_class = None
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """Create not allowed."""
        return CustomeResponse(
            {'msg': "NOT ALLOWED"},
            status=status.HTTP_400_BAD_REQUEST,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def send(self, request):
        """Send."""
        try:
            user_id = request.user.id

            businesscard_copy = request.data.copy()
            if 'businesscard' in request.data:

                businesscard = request.data['businesscard']

                business_card_class_create = BusinessViewSet.as_view(
                    {'post': 'create'})
                business_card_class_update = BusinessViewSet.as_view(
                    {'post': 'update'})
                position = 0
                for raw_data in businesscard:

                    # Create the business card
                    if raw_data["operation"] == 'add':
                        business_data = []
                        if raw_data["json_data"]:
                            # execute all business card
                            for items in raw_data["json_data"]:
                                data = {}
                                data['user_id'] = user_id
                                try:
                                    data['bcard_json_data'] = items[
                                        'bcard_json_data']
                                except KeyError:
                                    data['bcard_json_data'] = ''

                                # Local business card id
                                try:
                                    local_business_id = items['local_business_id']
                                except:
                                    local_business_id = ''

                                business_card_response = business_card_class_create(
                                    request, 1, data)
                                business_card_response = business_card_response.data
                                if business_card_response["status"]:
                                    try:
                                        bcard_id = business_card_response[
                                            "data"]["id"]
                                    except KeyError:
                                        bcard_id = business_card_response["data"]
                                    business_data.append(
                                        {
                                            "local_business_id": local_business_id,
                                            "bcard_id": bcard_id
                                        }
                                    )
                                else:
                                    business_data.append(
                                        {
                                            "local_business_id": local_business_id,
                                            "bcard_id": business_card_response["data"]
                                        }
                                    )
                            businesscard_copy['businesscard'][
                                position]['json_data'] = business_data
                    # End

                    # Update the business card
                    if raw_data["operation"] == 'update':
                        business_data = []
                        if raw_data["json_data"]:
                            # execute all business card
                            for items in raw_data["json_data"]:
                                data = {}
                                data['user_id'] = user_id
                                try:
                                    data['bcard_json_data'] = items[
                                        'bcard_json_data']
                                except KeyError:
                                    data['bcard_json_data'] = ''

                                # Local business card id
                                try:
                                    local_business_id = items['local_business_id']
                                except KeyError:
                                    local_business_id = ''
                                # End

                                # Local business card id
                                try:
                                    data['bcard_id'] = items['bcard_id']
                                except KeyError:
                                    data['bcard_id'] = ''
                                # End
                                if data['bcard_id']:
                                    business_card_response = business_card_class_update(
                                        request, None, 1, data)
                                    business_card_response = business_card_response.data
                                    if business_card_response["status"]:

                                        try:
                                            bcard_id = business_card_response[
                                                "data"]["id"]
                                        except KeyError:
                                            bcard_id = business_card_response[
                                                "data"]
                                        business_data.append(
                                            {
                                                "local_business_id": local_business_id,
                                                "bcard_id": bcard_id
                                            }
                                        )
                                    else:
                                        business_data.append(
                                            {
                                                "local_business_id": local_business_id,
                                                "bcard_id": business_card_response["data"]
                                            }
                                        )
                                else:
                                    business_data.append(
                                        {
                                            "local_business_id": local_business_id,
                                            "bcard_id": 'provide business card id to update'
                                        }
                                    )
                            businesscard_copy['businesscard'][
                                position]['json_data'] = business_data

                    position = position + 1

            if 'link_bcard_to_identifier' in request.data:

                link_bcard_to_identifier = request.data['link_bcard_to_identifier']
                link_bcard_to_identifier_class = BusinessCardIdentifierViewSet()
                bcard_link_data = []
                for items in link_bcard_to_identifier:

                    items['user_id'] = user_id

                    response = link_bcard_to_identifier_class.create(
                        request, 1, items)
                    if response["status"]:
                        bcard_link_data.append({"msg": "atached"})
                    else:
                        bcard_link_data.append({"item": items, "msg": response})

                businesscard_copy['link_bcard_to_identifier'] = bcard_link_data

            return CustomeResponse(businesscard_copy, status=status.HTTP_200_OK)
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
    def updatemultiplerecord(self, request):
        """Update multiple settings in case of offline."""
        try:
            getkey = request.DATA
            updated_settings = []
            non_updated_settings = []
            for key, value in getkey.items():
                try:
                    UserSetting.objects.filter(
                        user_id=request.user.id,
                        setting_id__key=key).update(
                        value=value)
                    updated_settings.append(key)
                except Exception:
                    non_updated_settings.append(key)
            return CustomeResponse({"updated_settings": updated_settings,
                                    "non_updated_settings": non_updated_settings},
                                   status=status.HTTP_200_OK)
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
    def sendVactionCard(self, request):
        """Bulk Vacation card update and create."""
        try:
            user_id = request.user.id
            try:
                vacation_card = request.data['vacationcard']
                vacationcard_copy = request.data.copy()
            except KeyError:
                vacation_card = ''
                vacationcard_copy = ''

            final_return_data = {}

            if vacation_card:
                vacation_card_class_create = VacationCardViewSet.as_view(
                    {'post': 'create'})
                vacation_card_class_update = VacationCardViewSet.as_view(
                    {'post': 'update'})
                position = 0
                for raw_data in vacation_card:
                    # i=0
                    # Create the Vacation card
                    if raw_data["operation"] == 'add':
                        vacation_data = []
                        if raw_data["json_data"]:
                            # execute all vacation card
                            vcard_data = []
                            stop_data = []
                            for items in raw_data["json_data"]:
                                data = {}
                                data['user_id'] = user_id
                                try:
                                    data['vacation_name'] = items['vacation_name']
                                except KeyError:
                                    data['vacation_name'] = ''

                                # Local vacation card id
                                try:
                                    data['vacation_trips'] = items[
                                        'vacation_trips']
                                except KeyError:
                                    data['vacation_trips'] = ''
                                # End
                                try:
                                    local_vacation_id = items['local_vacation_id']
                                except KeyError:
                                    local_vacation_id = ''

                                vacation_card_response = vacation_card_class_create(
                                    request, 1, data)
                                vacation_card_response = vacation_card_response.data
                                if vacation_card_response["status"]:
                                    try:
                                        vcard_id = vacation_card_response

                                    except KeyError:
                                        vcard_id = vacation_card_response

                                    vacation_data.append(
                                        {"local_vacation_id": local_vacation_id, "vcard_id": vcard_id})
                                else:

                                    vacation_data.append(
                                        {"local_vacation_id": local_vacation_id, "vcard_id": vacation_card_response})
                                # i=i+1
                            vacationcard_copy['vacationcard'][
                                position]['json_data'] = vacation_data
                    # End

                    # Update the vacation card
                    if raw_data["operation"] == 'update':
                        vacation_data = []
                        if raw_data["json_data"]:
                            # execute all vacation card
                            for items in raw_data["json_data"]:

                                data = {}
                                data['user_id'] = user_id
                                try:
                                    data['vacation_name'] = items['vacation_name']
                                except KeyError:
                                    data['vacation_name'] = ''

                                # Local vacation card id
                                try:
                                    data['vacation_trips'] = items[
                                        'vacation_trips']
                                except KeyError:
                                    data['vacation_trips'] = ''

                                # Local vacation card id
                                try:
                                    local_vacation_id = items['local_vacation_id']
                                except KeyError:
                                    local_vacation_id = ''
                                # End

                                # Local vacation card id
                                try:
                                    data['vcard_id'] = items['vcard_id']
                                except KeyError:
                                    data['vcard_id'] = ''
                                # End
                                if data['vcard_id']:

                                    vacation_card_response = vacation_card_class_update(
                                        request, None, 1, data)
                                    vacation_card_response = vacation_card_response.data
                                    if vacation_card_response["status"]:

                                        try:
                                            vcard = {}
                                            vcard_id = vacation_card_response

                                        except KeyError:
                                            print "except"
                                            vcard_id = vacation_card_response
                                        vacation_data.append(
                                            {"local_vacation_id": local_vacation_id, "vcard_id": vacation_card_response})
                                    else:
                                        vacation_data.append(
                                            {"local_vacation_id": local_vacation_id, "vcard_id": vacation_card_response})
                                else:
                                    vacation_data.append(
                                        {"local_business_id": local_vacation_id, "vcard_id": 'provide vacation card id to update'})
                            vacationcard_copy['vacationcard'][
                                position]['json_data'] = vacation_data

                    position = position + 1
            return CustomeResponse(vacationcard_copy, status=status.HTTP_200_OK)
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


# End


#  Fetch data from server
    @list_route(methods=['get'],)
    def receive(self, request):
        pass
