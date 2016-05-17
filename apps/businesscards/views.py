# --------- Import Python Modules ----------- #
import json
import validictory
import collections
# ------------------------------------------- #
# ------------ Third Party Imports ---------- #
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import rest_framework.status as status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import list_route
from django.core.exceptions import ObjectDoesNotExist
from logging import getLogger
# ------------------------------------------- #
# ----------------- Local app imports ------ #
from models import (
    BusinessCard,
    # BusinessCardTemplate,
    BusinessCardIdentifier,
    Identifier,
    BusinessCardSkillAvailable,
    BusinessCardAddSkill
)
from serializer import (
    BusinessCardSerializer,
    BusinessCardIdentifierSerializer,
    BusinessCardSkillAvailableSerializer,
    BusinessCardAddSkillSerializer,
    BusinessCardSummarySerializer
)
from apps.contacts.serializer import ContactsSerializer
from apps.contacts.models import Contacts, ContactMedia
from apps.identifiers.serializer import BusinessIdentifierSerializer
from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse, rawResponse
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION
from apps.users.models import User
from apps.vacationcard.models import VacationCard
from apps.folders.views import FolderViewSet
from apps.sendrequest.views import SendAcceptRequest
from apps.folders.models import Folder, FolderContact
from apps.folders.serializer import FolderSerializer
from serializer import (
    BusinessCardWithIdentifierSerializer,
    SearchBusinessCardWithIdentifierSerializer
)
from functions import createDuplicateBusinessCard
import re

logger = getLogger(__name__)
ravenclient = getattr(settings, 'RAVEN_CLIENT', None)


# ---------------- Business Card Summary ---------------------- #
class CardSummary(APIView):
    """View to card summary."""

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BusinessCard.objects.all()

    def get(self, request):
        """Get all business_cards."""
        try:
            bcard_id = self.request.data['bcard_id']
        except KeyError:
            return CustomeResponse(
                {
                    'msg': 'bcard_id is required.'
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
                validate_errors=1
            )
        try:
            queryset = self.queryset.filter(id=bcard_id)

            serializer = BusinessCardSummarySerializer(queryset, many=True)
            dt = serializer.data
            for d in serializer.data:
                dt = d
                businesscard = BusinessCard(id=bcard_id)
                break
            return CustomeResponse(dt, status=status.HTTP_200_OK)
        except:
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

    def post(self, request, format=None):
        """Post method not allowed."""
        return CustomeResponse(
            {
                'msg': 'POST method not allowed'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            validate_errors=1
        )


class BusinessCardIdentifierViewSet(viewsets.ModelViewSet):
    """Bsuinesscardidentifier viewsets."""

    queryset = BusinessCardIdentifier.objects.all()
    serializer_class = BusinessCardIdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # --------------Method: GET----------------------------- #

    def list(self, request):
        """Get attached business_card with Identifier."""
        user_id = request.user
        try:
            self.queryset = Identifier.objects.all().filter(user_id=user_id)
            """
            get all identifiers from identifiers table.
            """
            serializer = BusinessIdentifierSerializer(
                self.queryset,
                many=True
            )
            if serializer:
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': "No Data Found"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
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

    def create(self, request, call_from_function=None, offline_data=None):
        """Attach business_card to identifier."""
        try:
            try:
                op = request.data['op']
            except KeyError as e:
                logger.error("Caught KeyError in {}, {}".format(__file__, e))
                op = None

            if op == 'change':
                try:
                    businesscard_id = request.data['businesscard_id']
                    if businesscard_id:
                        businesscardidentifier_detail = BusinessCardIdentifier.objects.filter(
                            businesscard_id=businesscard_id)
                        businesscardidentifier_detail.delete()
                except KeyError as e:
                    logger.error("Caught KeyError in {}, {}".format(
                        __file__,
                        e
                    )
                    )

            # TODO check business card and identifier belongs to authentic user
            # --------- END ----- #
            data = {}
            if call_from_function:
                data = offline_data
            else:
                data = request.data
            serializer = BusinessCardIdentifierSerializer(
                data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                BusinessCard.objects.filter(
                    id=data['businesscard_id']
                ).update(
                    status=1,
                    is_active=1
                )
                if call_from_function:
                    return rawResponse(
                        serializer.data,
                        status=True,
                        status_code=status.HTTP_201_CREATED
                    )
                else:
                    return CustomeResponse(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
            else:
                if call_from_function:
                    return rawResponse(serializer.errors)
                else:
                    return CustomeResponse(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
        except:
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
    def unlinkIdentifier(self, request):
        """Unlink Identifier from businesscard."""
        try:
            try:
                identifier_id = request.data['identifier_id']
            except KeyError:
                logger.error(
                    "Caught KeyError exception, identifier_id not given in {}".
                    format(__file__)
                )
                return CustomeResponse(
                    {
                        'msg': 'identifier_id is required.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )

            try:
                businesscard_id = request.data['bcard_id']
            except KeyError:
                logger.error(
                    "Caught KeyError exception, bcard_id not given in {}".
                    format(__file__)
                )
                return CustomeResponse(
                    {
                        'msg': 'bcard_id is required.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
            getbusinessacard_identifier_data = BusinessCardIdentifier.objects.filter(
                identifier_id=identifier_id, businesscard_id=businesscard_id)

            # Unlink Businesscard Identifier status 0 in Businesscardidentifier
            # table#
            if getbusinessacard_identifier_data:
                getbusinessacard_identifier_data.delete()
                return CustomeResponse(
                    {
                        'msg': "Business card has been unlinked with identifiers."
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': "Identifier not attached."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
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

    def destroy(self, request, pk=None):
        """
        Delete Identifiers it will first inactive the businesscard.

        then delete the linking of identifier with businesscard
        in businesscard_identifier table then delete the identifeirs
        in identifier table.
        """
        try:
            identifier_data = Identifier.objects.get(id=pk)

            if identifier_data:
                businesscard_identifier_data = BusinessCardIdentifier.objects.filter(
                    identifier_id=identifier_data)
                if businesscard_identifier_data:

                    businesscard_id = businesscard_identifier_data[
                        0].businesscard_id.id
                    BusinessCard.objects.filter(
                        id=businesscard_id).update(status=0, is_active=0)
                    businesscard_identifier_data.delete()
                identifier_data.delete()
                return CustomeResponse(
                    {
                        'msg': "Business card has been Inactive and \
                        identifiers has been deleted "
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': "Businesscard Identifier Id not found"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
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

    @list_route(methods=['post'])
    def searchIdentifier(self, request):
        """Search business_card by email ,name and Identifiers."""
        from functions import searchjson
        user_id = request.user.id

        try:
            value = request.data['name']
        except KeyError as e:
            logger.error("Caught KeyError in {}, value {}".format(__file__), e)
            ravenclient.captureException()

            value = ''
            return CustomeResponse({'msg': "Please provide name"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        # search by firstname and lastname or by identifier#
        try:
            if not re.match("[^@]+@[^@]+\.[^@]+", value):

                identifier_data = BusinessCard.objects.filter(
                    status=1, identifiers_data__identifier_id__identifier=value)
                bcard_id = None

                if identifier_data:
                    bcard_id = identifier_data[0].id
                    bcard_id = bcard_id
                name = "firstname_lastname"
                user_id = ''

                searchname_data = searchjson(name, value, user_id, bcard_id)
                if identifier_data or searchname_data:
                    name_serializer = SearchBusinessCardWithIdentifierSerializer(
                        searchname_data, many=True, context={'search': "name"})
                    businesscard_by_identifier_serializer = SearchBusinessCardWithIdentifierSerializer(
                        identifier_data, many=True, context={'search': "identifier"})
                    return CustomeResponse(
                        {
                            'search_business_cards': businesscard_by_identifier_serializer.data + name_serializer.data,
                        },
                        status=status.HTTP_200_OK)

                else:
                    return CustomeResponse(
                        {'msg': "Businesscard not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

            # Search by email #
            else:
                userdata = User.objects.filter(email=value).values()

                if userdata:
                    user_id = userdata[0]['id']
                    name = "email"
                    data = searchjson(name, value, user_id)
                    if data:
                        serializer = SearchBusinessCardWithIdentifierSerializer(
                            data, many=True, context={'search': "email"})
                        return CustomeResponse({'search_business_cards_by_email': serializer.data},
                                               status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse(
                            {'msg': "email not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

                else:
                    name = "email"
                    user_id = ""
                    data = searchjson(name, value)
                    if data:
                        serializer = SearchBusinessCardWithIdentifierSerializer(
                            data, many=True, context={'search': "email"})
                        return CustomeResponse({'search_business_cards_by_email': serializer.data},
                                               status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse(
                            {'msg': "email not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        except Exception:
            logger.critical("Caught Exception ", exc_info=True)

        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

# BusinessCard History


class BusinessCardHistoryViewSet(viewsets.ModelViewSet):
    """BusinessCardHistory viewsets."""

    #queryset = BusinessCardHistory.objects.all()
    #serializer_class = BusinessCardHistorySerializer

    def list(self, request):
        """Get businesscard data."""
        try:
            bid = self.request.query_params.get('bid', None)
            if bid:
                self.queryset = self.queryset.filter(
                    businesscard_id=bid).order_by('updated_date').values()

                if self.queryset:
                    data = {}
                    data['side_first'] = []
                    data['side_second'] = []

                    # for items in self.queryset:
                    #   data['side_first'].append({"bcard_json_data":items['bcard_json_data']['side_first']['basic_info']})
                    #  data['side_second'].append({"bcard_json_data":items['bcard_json_data']['side_second']['contact_info']})
            serializer = self.serializer_class(
                self.queryset,
                many=True
            )
            if serializer:
                return CustomeResponse(
                    self.queryset,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
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

    def create(self, request):
        """Create businesscard history."""
        return CustomeResponse(
            {
                'msg': "Update method does not allow"
            },
            status=status.HTTP_400_BAD_REQUEST,
            validate_errors=1
        )

    def update(self, request, pk=None):
        """Update not implemented."""
        return CustomeResponse(
            {
                'msg': "Update method does not allow"
            },
            status=status.HTTP_400_BAD_REQUEST,
            validate_errors=1
        )

# BusinessCard Available Skills


class BusinessCardSkillAvailableViewSet(viewsets.ModelViewSet):
    """Businesscard skill."""

    queryset = BusinessCardSkillAvailable.objects.all()
    serializer_class = BusinessCardSkillAvailableSerializer

    def list(self, request):
        """List businesscard skills."""
        try:
            skill = self.request.query_params.get('skill', None)
            if skill:
                self.queryset = self.queryset.filter(
                    skill_name__istartswith=skill
                )

            serializer = self.serializer_class(
                self.queryset,
                many=True
            )

            if serializer and self.queryset:
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': 'no data found'
                    },
                    status=status.HTTP_200_OK,
                    validate_errors=1
                )
        except:
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

    def create(self, request):
        """Create businesscard skill."""
        try:
            serializer = BusinessCardSkillAvailableSerializer(
                data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
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

    def update(self, request, pk=None):
        """Update not allow."""
        return CustomeResponse(
            {
                'msg': "Update method does not allow"
            },
            status=status.HTTP_400_BAD_REQUEST,
            validate_errors=1
        )

    @list_route(methods=['get'],)
    def allSkills(self, request):
        """Get list of skills."""
        try:
            skillsAvailable = BusinessCardSkillAvailable.objects.all()
            serializer = BusinessCardSkillAvailableSerializer(
                skillsAvailable,
                many=True
            )
            return CustomeResponse(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except:
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

    # Add Skills to Business Card


class BusinessCardAddSkillViewSet(viewsets.ModelViewSet):
    """BusinessCardAddSkill viewsets."""

    queryset = BusinessCardAddSkill.objects.all()
    serializer_class = BusinessCardAddSkillSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # --------------Method: GET----------------------------- #

    def list(self, request):
        """List  skills in businesscard."""
        bcard_id = self.request.query_params.get('bcard_id', None)
        if bcard_id:
            self.queryset = self.queryset.filter(businesscard_id=bcard_id).order_by('skill_name')
        serializer = self.serializer_class(self.queryset, many=True)
        if serializer and self.queryset:
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {'msg': 'no data found'}, status=status.HTTP_200_OK, validate_errors=1)

    @list_route(methods=['get'],)
    def bcard_with_skills(self, request):
        """businesscards with added skills."""
        user_id = request.user.id
        bcard_ids = []
        skill_name = []
        final_list = []
        counter = 0
        if user_id:
            self.queryset = BusinessCardAddSkill.objects.filter(
                user_id=user_id)
            for items in self.queryset:
                if items.businesscard_id.id not in bcard_ids:
                    final_list.append(
                        {'bcard_id': items.businesscard_id.id, 'skill_name': items.skill_name})
                else:
                    list_val = [i for i, x in enumerate(final_list) if x[
                        'bcard_id'] == items.businesscard_id.id]
                    final_list[list_val[0]]['skill_name'] = str(
                        final_list[list_val[0]]['skill_name']) + ', ' + str(items.skill_name)
                bcard_ids.append(items.businesscard_id.id)

        serializer = self.serializer_class(self.queryset, many=True)
        if serializer and self.queryset:
            return CustomeResponse(final_list, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {'msg': 'no data found'}, status=status.HTTP_200_OK, validate_errors=1)

    def retrieve(self, request, pk=None):
        """Retrieve method not allowed."""
        return CustomeResponse({'msg': 'GET method not allowed'},
                               status=status.HTTP_405_METHOD_NOT_ALLOWED,
                               validate_errors=1)

    def create(self, request):
        """Add skills in businesscard."""
        try:
            tempData = {}
            tempData['user_id'] = request.user.id
            tempData['businesscard_id'] = request.data['businesscard_id']
            tempData['skill_name'] = request.data['skill_name'].split(',')
            serializer = BusinessCardAddSkillSerializer(
                data=tempData,
                context={
                    'request': request
                }
            )

            if serializer.is_valid():
                businesscard_id = tempData['businesscard_id']
                user_id = tempData['user_id']
                skill_name = tempData['skill_name']

                BusinessCardAddSkill.objects.filter(
                    businesscard_id=businesscard_id).delete()
                for item in skill_name:
                    data = {}
                    data['skill_name'] = item
                    data['user_id'] = user_id
                    data['businesscard_id'] = businesscard_id
                    serializer = BusinessCardAddSkillSerializer(
                        data=data,
                        context={
                            'request': request
                        }
                    )
                    serializer.is_valid()
                    serializer.save()
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
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

    def update(self, request, pk=None):
        """Update not allowed."""
        return CustomeResponse(
            {
                'msg': "Update method does not allow"
            },
            status=status.HTTP_400_BAD_REQUEST,
            validate_errors=1
        )


class BusinessViewSet(viewsets.ModelViewSet):
    """Business card viewset."""

    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardWithIdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    vacation_data = ''

    def list(self, request):
        """List businesscards."""
        user_id = request.user.id
        try:
            published = self.request.query_params.get('published', None)
            business_id = self.request.query_params.get('business_id', None)
            is_active = self.request.query_params.get('is_active', None)
            vacation_data_check = 0
            # ---------------------- Filter ------------------------ #
            if published is not None and user_id is not None:
                if published == '0':
                    self.queryset = self.queryset.select_related(
                        'user_id'
                    ).filter(
                        user_id=user_id,
                        status=0,
                        is_active=1
                    )
                elif published == '1':
                    self.queryset = self.queryset.select_related(
                        'user_id'
                    ).filter(
                        user_id=user_id,
                        status=1,
                        is_active=1
                    )

            elif is_active is not None and user_id is not None:
                self.queryset = self.queryset.select_related(
                    'user_id'
                ).filter(
                    user_id=user_id,
                    is_active=0,
                    status=0
                )

            elif user_id is not None and business_id == 'all':
                    # ----------------- All user business card ---------- #
                self.queryset = self.queryset.select_related(
                    'user_id'
                ).filter(
                    user_id=user_id
                )
                self.vacation_data = VacationCard.objects.all().filter(
                    user_id=user_id
                )
                vacation_data_check = 1
            elif user_id is not None:
                self.queryset = self.queryset.select_related(
                    'user_id'
                ).filter(
                    user_id=user_id
                )

            # ------------------------- End ------------------------- #
            serializer = self.serializer_class(self.queryset, many=True)

            if vacation_data_check:
                data = {}
                data['business_cards'] = serializer.data
                data['vacation_cards'] = ""
                vacation_data = []
                for item in self.vacation_data:
                    vacation_data.append(
                        {"id": item.id, "user_id": item.user_id.id})
                data['vacation_cards'] = vacation_data
                return CustomeResponse(
                    data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
        except:
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

    def retrieve(
        self,
        request,
        pk=None,
        contact_id_new=None,
        call_from_function=None
    ):
        """Get businesscard."""
        user_id = request.user.id
        try:
            bcard_obj = get_object_or_404(
                BusinessCard,
                pk=pk,
                user_id=user_id
            )
            serializer = self.serializer_class(
                bcard_obj,
                context={'request': request}
            )
            media = ContactMedia.objects.filter(
                contact_id=contact_id_new,
                front_back__in=[1, 2],
                status=1
            ).values(
                'img_url',
                'front_back'
            )
            data = {}
            data = serializer.data
            if media:
                try:
                    for item in media:
                        if item['front_back'] == 1:
                            data['bcard_image_frontend'] = str(
                                settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(item['img_url'])
                        elif item['front_back'] == 2:
                            data['bcard_image_backend'] = str(
                                settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(item['img_url'])
                except Exception as e:
                    logger.error(
                        "Caught Exception in {}, {}".format(
                            __file__, e))
                    ravenclient.captureException()

            if call_from_function:
                return data
            else:
                return CustomeResponse(
                    data,
                    status=status.HTTP_200_OK
                )
        except:
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

    def create(self, request, call_from_func=None, offline_data=None):
        """Create new business card."""
        try:
            user_id = request.user.id

            try:
                validictory.validate(
                    request.data["bcard_json_data"],
                    BUSINESS_CARD_DATA_VALIDATION
                )
            except validictory.ValidationError as e:
                logger.error(
                    "Caught validictory.ValidationError in {}, {}".format(
                        __file__, e)
                )
                ravenclient.captureException()

                return CustomeResponse(
                    {
                        'msg': e.message
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
            except validictory.SchemaError as e:
                logger.error(
                    "Caught validictory.ValidationError in {}, {}".format(
                        __file__, e
                    )
                )
                ravenclient.captureException()

                return CustomeResponse(
                    {
                        'msg': e.message
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
            except KeyError:
                logger.error(
                    "Caught KeyError in {}".format(
                        __file__
                    ),
                    exc_info=True
                )
                return CustomeResponse(
                    {
                        'msg': "Please provide bcard_json_data in json format"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )

            if call_from_func:
                # Call from offline app
                tempData = offline_data
            else:
                tempData = request.data.copy()
                tempData["user_id"] = user_id

            serializer = BusinessCardSerializer(
                data=tempData,
                context={'request': request}
            )

            if serializer.is_valid():
                contact_serializer = ContactsSerializer(
                    data=tempData,
                    context={'request': request}
                )
                if contact_serializer.is_valid():
                    business = serializer.save()
                    contact_serializer.validated_data[
                        'businesscard_id'] = business
                    contact_serializer = contact_serializer.save()

                    bcards = BusinessCard.objects.get(id=business.id)
                    contact = bcards.contact_detail
                    user = request.user
                    # -------------- Save Notes ------------ #
                    data_new = serializer.data.copy()

                    if "business_notes" in request.data:
                        try:
                            from apps.notes.models import Notes
                            if "note_frontend" in request.data[
                                    "business_notes"]:
                                note_frontend_obj = Notes(
                                    user_id=user,
                                    contact_id=contact,
                                    note=request.data["business_notes"][
                                        'note_frontend'],
                                    bcard_side_no=1)
                                note_frontend_obj.save()
                            if "note_backend" in request.data[
                                    "business_notes"]:
                                note_frontend_obj = Notes(
                                    user_id=user,
                                    contact_id=contact,
                                    note=request.data["business_notes"][
                                        'note_backend'],
                                    bcard_side_no=2)
                                note_frontend_obj.save()
                        except Exception as e:
                            logger.error(
                                "Caught Exception in {}, {}".format(
                                    __file__,
                                    e
                                )
                            )
                            ravenclient.captureException()

                    data_new["business_notes"] = serializer.fetch_notes(bcards)
                    # -------------------------End------------ #

                    # Assign  first created business card to created default
                    # folder
                    queryset_folder = Folder.objects.filter(
                        user_id=user_id,
                        foldertype='PR',
                        businesscard_id__isnull=True
                    )
                    if not queryset_folder:
                        folder_view = FolderViewSet.as_view({'post': 'create'})
                        offline_data = {}
                        offline_data['businesscard_id'] = business.id
                        offline_data['foldername'] = 'PR Folder'
                        folder_view = folder_view(request, offline_data)
                        data_new["folder_info"] = folder_view.data['data']
                    else:
                        queryset_folder.update(
                            businesscard_id=business.id
                        )
                        # data_new["folder_info"]=folder_info
                    # -------------------- End ------------------- #
                else:
                    return CustomeResponse(
                        contact_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )

                return CustomeResponse(
                    data_new,
                    status=status.HTTP_201_CREATED
                )

            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
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

    def update(self, request, pk=None, call_from_func=None, offline_data=None):
        """Update Businesscard."""
        # -------------- First Validate the json contact data ------ #
        try:
            validictory.validate(
                request.data["bcard_json_data"], BUSINESS_CARD_DATA_VALIDATION)
        except validictory.ValidationError as error:
            logger.error(
                "Caught validictory.ValidationError in {}, {}".format(
                    __file__, error
                )
            )
            return CustomeResponse(
                {
                    'msg': error.message
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except validictory.SchemaError as error:
            logger.error(
                "Caught validictory.ValidationError in {}, {}".format(
                    __file__, error
                )
            )
            return CustomeResponse(
                {
                    'msg': error.message
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except KeyError:
            logger.error(
                "Caught KeyError in {}, {}".format(
                    __file__
                ),
                exc_info=True
            )
            return CustomeResponse(
                {
                    'msg': "Please provide bcard_json_data in json format"
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        # End
        try:
            if call_from_func:
                data = offline_data
                pk = offline_data["bcard_id"]
                user_id = offline_data["user_id"]
            else:
                data = request.data.copy()
                user_id = request.user.id
                data['user_id'] = request.user.id
            try:
                bcards = BusinessCard.objects.get(id=pk)
            except BusinessCard.DoesNotExist:
                if call_from_func:
                    return rawResponse('record not found')
                else:
                    return CustomeResponse(
                        {
                            'msg': 'record not found'
                        },
                        status=status.HTTP_404_NOT_FOUND,
                        validate_errors=1
                    )

            serializer = BusinessCardSerializer(
                bcards, data=data, context={'request': request})
            if serializer.is_valid():
                contact = Contacts.objects.get(businesscard_id=pk)
                contact_serializer = ContactsSerializer(
                    contact, data=data, context={'request': request})
                if contact_serializer.is_valid():
                    serializer.save()
                    contact_serializer.save()
                    user = User.objects.get(id=user_id)
                    # -------------- Save Notes --------------- #
                    data_new = serializer.data.copy()
                    # try:
                    if "business_notes" in request.data:
                        from apps.notes.models import Notes
                        if "note_frontend" in request.data["business_notes"]:
                            try:
                                note_frontend_obj = Notes.objects.get(
                                    user_id=user,
                                    contact_id=contact,
                                    bcard_side_no=1)
                            except ObjectDoesNotExist:
                                note_frontend_obj = Notes(
                                    user_id=user,
                                    contact_id=contact,
                                    bcard_side_no=1)
                            note_frontend_obj.note = request.data[
                                "business_notes"]['note_frontend']
                            note_frontend_obj.save()

                        if "note_backend" in request.data["business_notes"]:
                            try:
                                note_frontend_obj = Notes.objects.get(
                                    user_id=user,
                                    contact_id=contact,
                                    bcard_side_no=2)
                            except ObjectDoesNotExist:
                                note_frontend_obj = Notes(
                                    user_id=user,
                                    contact_id=contact,
                                    bcard_side_no=2)
                            note_frontend_obj.note = request.data[
                                "business_notes"]['note_backend']
                            note_frontend_obj.save()

                    # except:
                    #    pass
                    data_new["business_notes"] = serializer.fetch_notes(bcards)
                else:
                    return CustomeResponse(
                        contact_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )

                return CustomeResponse(
                    data_new,
                    status=status.HTTP_200_OK
                )

            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
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

    # ---------------------------- Duplicate the business card --------------- #
    @list_route(methods=['post'],)
    def duplicate(self, request):
        """Duplicate businesscard."""

        user_id = request.user.id

        try:
            bcard_id = request.data["bcard_id"]
        except KeyError:
            return CustomeResponse(
                {
                    "msg": "Please provide bcard_id."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        try:
            data = createDuplicateBusinessCard(bcard_id, user_id)

            if data:
                data = self.retrieve(
                    request,
                    pk=data['bcards_id_new'],
                    contact_id_new=data['contact_id_new'],
                    call_from_function=1
                )
            else:
                return CustomeResponse(
                    {
                        "msg": "some problem occured on server side."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
            return CustomeResponse(data, status=status.HTTP_200_OK)
        except:
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

    def mergeSkills(self, m, t, u):
        """Merge Skills."""
        try:
            target_bcard = BusinessCardAddSkill.objects.filter(
                businesscard_id__in=m, user_id=u)
            if target_bcard:
                target_bcard.update(businesscard_id=t)
            return target_bcard
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return False

    def mergeDict(self, s, f):
        """Merge business card contact."""
        try:
            for k, v in f.iteritems():
                if isinstance(v, collections.Mapping):
                    r = self.mergeDict(s.get(k, {}), v)
                    s[k] = r
                elif isinstance(v, list):
                    result = []
                    """ TODO : optimization """

                    if k == 'basic_info':
                        for valf in v:
                            if 'keyName' in valf:
                                for vals in s.get(k, {}):
                                    if valf['keyName'] in vals.values() and vals['value'] != "" and valf[
                                            'value'] == "":
                                        valf['value'] = vals['value']
                                result.append(valf)
                        """ Reverse loop is for check  extra data in
                        second business card.
                        """
                        for vals1 in s.get(k, {}):
                            if 'keyName' in vals1:
                                check = 0
                                for valf1 in v:
                                    if vals1['keyName'] in valf1.values():
                                        check = 1
                                if not check:
                                    result.append(vals1)
                    else:
                        v.extend(s.get(k, {}))
                        for myDict in v:
                            if myDict not in result:
                                result.append(myDict)

                    s[k] = result
                else:
                    """
                    If the key is blank in first business card then
                    second business card value assign to it
                    """
                    if not v and s.get(k, {}):
                        pass
                    else:
                        s[k] = f[k]
            return s
        except:
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
    def merge(self, request):
        """Merge Businesscard."""
        user_id = request.user.id

        try:
            merge_bcards_ids = request.data["merge_bcards_ids"]
        except KeyError:
            logger.error(
                "Caught KeyError exception, merge_bcards_ids in {} \
                by user {}".
                format(__file__, user_id)
            )
            return CustomeResponse(
                {
                    "msg": "merge_bcards_ids is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        try:
            target_bcard_id = request.data["target_bcard_id"]
        except KeyError:
            logger.error(
                "Caught KeyError exception, target_bcard_id in {} \
                by user {}".
                format(__file__, user_id)
            )
            return CustomeResponse(
                {
                    "msg": "target_bcard_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        # Get the  target_bcard_id and merge_bcards_ids data
        try:
            target_bacard = BusinessCard.objects.select_related().get(
                id=target_bcard_id, user_id=user_id)
            first_json = json.loads(json.dumps(
                target_bacard.contact_detail.bcard_json_data))
            # make sure target_bcard_id not in merge_bcards_ids
            if target_bcard_id not in merge_bcards_ids:
                merge_bcards = BusinessCard.objects.filter(
                    id__in=merge_bcards_ids, user_id=user_id).all()

                for temp in merge_bcards:
                    contact_json_data = temp.contact_detail.bcard_json_data
                    if contact_json_data:
                        try:
                            second_json = json.loads(
                                json.dumps(contact_json_data))
                        except:
                            second_json = {}
                        third_json = second_json.copy()

                        self.mergeDict(third_json, first_json)

                        # assign the new json
                        target_bacard.contact_detail.bcard_json_data = third_json
                        target_bacard.contact_detail.save(force_update=True)
                        first_json = third_json
                #  TODO Delete the  merge_bcards_ids
                if merge_bcards:
                    self.mergeSkills(merge_bcards_ids,
                                     target_bcard_id, user_id)
                    merge_bcards.delete()
                else:
                    return CustomeResponse(
                        {
                            "msg": "merge_bcards_ids does not exist."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
                # End

                self.queryset = self.queryset.select_related(
                    'user_id').filter(user_id=user_id, id=target_bcard_id)
                serializer = self.serializer_class(self.queryset, many=True)
                data = {}
                data['business_cards'] = serializer.data
                return CustomeResponse(data, status=status.HTTP_200_OK)

            else:
                return CustomeResponse(
                    {
                        "msg": "Please provide correct target_bcard_id"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
        except:
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
    def delete(self, request):
        """Delete business card."""
        user_id = request.user.id

        try:
            bcard_ids = request.data["bcard_ids"]

            business_card = BusinessCard.objects.filter(
                id__in=bcard_ids,
                user_id=user_id
            )
            if business_card:
                business_card.delete()
                return CustomeResponse(
                    {
                        "msg": "business card deleted successfully."
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        "msg": "business card does not exists."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                    validate_errors=1
                )

        except KeyError:
            logger.error(
                "Caught KeyError exception, bcard_ids in {} \
                by user {}".
                format(__file__, user_id)
            )
            ravenclient.captureException()
            return CustomeResponse(
                {
                    "msg": "bcard_ids is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except:
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
    # ----------------------------- End ---------------- #

    # Inactive Business Card
    @list_route(methods=['post'],)
    def inactive(self, request):
        """Inactive businesscard."""
        user_id = request.user.id

        try:
            bcards_id = request.data["bcards_ids"]
            BusinessCard.objects.filter(
                id__in=bcards_id,
                user_id=user_id
            ).update(
                is_active=0,
                status=0
            )
            return CustomeResponse(
                {
                    "msg": "Business cards has been inactive"
                },
                status=status.HTTP_200_OK
            )
        except KeyError:
            logger.error(
                "Caught KeyError exception, bcard_ids in {} \
                by user {}".
                format(__file__, user_id)
            )
            ravenclient.captureException()
            return CustomeResponse(
                {
                    "msg": "bcard_ids is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except:
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

    # ------------------------------- End -------------------- #

    # Reactive Business Card
    @list_route(methods=['post'],)
    def reactive(self, request):
        """reactive businesscard."""

        user_id = request.user.id

        try:
            bcard_id = request.data['bcard_id']
            bcard_identifier = BusinessCardIdentifier.objects.filter(
                businesscard_id=bcard_id,
                status=1
            )

            if bcard_identifier:
                businesscardcard_data = BusinessCard.objects.filter(
                    id=bcard_id
                ).update(
                    status=1,
                    is_active=1
                )

                if businesscardcard_data:
                    return CustomeResponse(
                        {
                            "msg": "Card has been Reactive successfully"
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return CustomeResponse(
                        {
                            "msg": "Card not found"
                        },
                        status=status.HTTP_404_NOT_FOUND,
                        validate_errors=1
                    )

            else:
                return CustomeResponse(
                    {
                        "msg": "Card can't be Reactive as your Business card \
                        is not attached with any identifiers."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except KeyError:
            logger.error(
                "Caught KeyError exception, bcard_id in {} \
                by user {}".
                format(__file__, user_id)
            )
            ravenclient.captureException()
            return CustomeResponse(
                {
                    "msg": "bcard_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except:
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

    def destroy(self, request, pk=None):
        """Delete not allow."""
        return CustomeResponse(
            {
                'msg': 'Delete method not allowed'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            validate_errors=1
        )

# create businessCard,folder and connections for grey contacts


class WhiteCardViewSet(viewsets.ModelViewSet):
    """Grey contact view set."""

    def create(self, request, from_white_contact=None, cid=None, sid=None):
        """create businesscard for invited user."""
        try:
            user_id = from_white_contact
            sender_user_id = sid
        except:
            user_id = None
        tempData = {}
        tempData["user_id"] = user_id

        try:
            serializer = BusinessCardSerializer(
                data=tempData, context={'request': request})

            if serializer.is_valid():
                business = serializer.save()
                # Assign  first created business card to created default folder
                queryset_folder = Folder.objects.filter(
                    user_id=user_id, foldertype='PR').values()
                sender_user_data = BusinessCard.objects.filter(
                    user_id=sender_user_id).values()

                if not queryset_folder:
                    user = business.user_id
                    user_id = user.id
                    offline_data = {}
                    offline_data['businesscard_id'] = business.id
                    offline_data['user_id'] = user_id
                    offline_data['foldername'] = 'PR'
                    serializer = FolderSerializer(
                        data=offline_data, context={'request': request})

                    if serializer.is_valid():
                        receiver_folder = serializer.save(user_id=user)
                        # data from signup form from web
                        Contacts.objects.filter(
                            id=cid).update(
                            businesscard_id=offline_data['businesscard_id'],
                            user_id=from_white_contact)

                        receiver_folder_id = Folder.objects.get(
                            id=receiver_folder.id)

                        receiver_contact_id = Contacts.objects.get(id=cid)

                        sender_data = FolderContact.objects.filter(
                            user_id=sid, contact_id=cid)

                        sender_folder_id = Folder.objects.get(
                            id=sender_data[0].folder_id.id)

                        sender_businesscard_id = sender_folder_id.businesscard_id

                        sender_contact_id = Contacts.objects.get(
                            businesscard_id=sender_businesscard_id)

                        # create connections - folderContact
                        contact_share = SendAcceptRequest()
                        contact_share.exchange_business_cards(
                            sender_folder=sender_folder_id,
                            sender_contact_id=sender_contact_id,
                            receiver_contact_id=receiver_contact_id,
                            receiver_folder=receiver_folder_id,
                            sender_user_id=sender_user_id,
                            receiver_user_id=user_id)

                        # send push notification
                        contact_share.send_push_notification(
                            "your business card accepted",
                            "b2g_accepted",
                            sender_user_id, cid
                        )

            #  ------------------- End ---------------- #

                return CustomeResponse(
                    offline_data, status=status.HTTP_201_CREATED)

            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
        except:
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
