"""Vacationcard view."""

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import logging


from models import (
    VacationTrip,
    VacationCard
)
from apps.businesscards.models import BusinessCardVacation
from serializer import (
    VacationTripSerializer,
    VacationEditTripSerializer,
    VacationCardSerializer,
    BusinessCardVacationSerializer,
    #SingleVacationCardSerializer
)
from apps.businesscards.serializer import SingleVacationCardSerializer
from serializer import (
    VacationCardMergeSerializer,
    VacationDuplicateSerializer
)
from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse
from functions import CreateDuplicateVacationCard

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)

# TODO: need to optimize this module.


class VacationCardViewSet(viewsets.ModelViewSet):
    """Vacation card viewset."""

    queryset = VacationTrip.objects.select_related().all()
    serializer_class = VacationTripSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        #"""List user vaction cards."""
        #try:

            user_id = request.user.id
            queryset = VacationCard.objects.select_related().all().filter(
                user_id=user_id
            )
            serializer = VacationCardSerializer(queryset, many=True)

            counter = 0
            for items in serializer.data:
                for key, value in items.items():
                    if key == 'vacation_trips':
                        counter1 = 1
                        no_of_stop = len(value)
                        for value1 in sorted(value):
                            if counter1 == 1:
                                serializer.data[counter][
                                    'vacation_start_date'] = value1['trip_start_date']
                            if no_of_stop == counter1:
                                serializer.data[counter][
                                    'vacation_end_date'] = value1['trip_end_date']

                            counter1 = counter1 + 1

                counter = counter + 1

            if serializer.data:
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': "No records found."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        # except Exception:
        #     logger.critical(
        #         "Caught exception in {}".format(__file__),
        #         exc_info=True
        #     )
        #     ravenclient.captureException()

        # return CustomeResponse(
        #     {
        #         "msg": "Can not process request. Please try later."
        #     },
        #     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     validate_errors=1
        # )

    def retrieve(self, request, vacationcard_id=None, call_from_function=None):
        """Retrive vacation card and its trips."""
        try:
            vacationtrip_duplicate_data = VacationTrip.objects.filter(
                vacationcard_id=vacationcard_id)
            serializer = VacationTripSerializer(
                vacationtrip_duplicate_data,
                many=True
            )
            data = {}
            data = serializer.data

            if call_from_function:
                return data
            else:
                return CustomeResponse(
                    data,
                    status=status.HTTP_200_OK
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

    def create(self, request, call_from_func=None, offline_data=None):

        if call_from_func:

            try:
                stops = offline_data['vacation_trips']
                vacation_name = offline_data['vacation_name']
                data = offline_data

            except KeyError:

                return CustomeResponse(
                    {
                        'msg': 'Please provide correct Json Format of vacation'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        else:
            try:
                stops = request.data['vacation_trips']
                vacation_name = request.data['vacation_name']
                data = request.data

            except KeyError:
                return CustomeResponse(
                    {
                        'msg': 'Please provide correct Json Format of vacation'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        try:
            VacationCardserializer = VacationCardSerializer(
                data=data,
                context={'request': request}
            )

            if VacationCardserializer.is_valid():
                vacationid = VacationCardserializer.save(
                    user_id=request.user, vacation_name=vacation_name)
                if stops and vacationid.id:
                    tempContainer = []
                    for data in stops:

                        tempdata = {}

                        tempdata["x"] = data

                        tempdata["x"]['vacationcard_id'] = vacationid.id

                        tempContainer.append(tempdata['x'])

                        serializer = VacationTripSerializer(
                            data=tempContainer,
                            many=True,
                            context={'local_date': 1}
                        )
                    if serializer.is_valid():
                        serializer.save(user_id=request.user)
                        return CustomeResponse(
                            serializer.data, status=status.HTTP_201_CREATED)

                    else:
                        vacationcard_data = VacationCard.objects.filter(
                            id=vacationid.id)
                        vacationcard_data.delete()
                        return CustomeResponse(
                            {
                                "msg": "check the required fields and trip dates"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                            validate_errors=1)
            else:

                return CustomeResponse(
                    VacationCardserializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
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
    def duplicate(self, request):
        """Duplicate vacation card."""
        user_id = request.user.id

        try:
            vacation_id = request.data['vacation_id']
            vcard_new = CreateDuplicateVacationCard(vacation_id, user_id)
            if vcard_new:
                data = self.retrieve(
                    request, vacationcard_id=vcard_new, call_from_function=1)
            else:
                return CustomeResponse(
                    {
                        "msg": "some problem occured on server side."},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
            return CustomeResponse(data, status=status.HTTP_201_CREATED)
        except KeyError:
            return CustomeResponse(
                {
                    "msg": "Please provide vcard_id and user_id"
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

    @list_route(methods=['post'],)
    def delete(self, request):

        user_id = request.user.id

        try:
            vcard_ids = request.data["vcard_ids"]

            vacation_card = VacationCard.objects.filter(
                id__in=vcard_ids, user_id=user_id)
            vacationtrip_info = VacationTrip.objects.filter(
                vacationcard_id__in=vcard_ids, user_id=user_id)
            businesscardvacation_info = BusinessCardVacation.objects.filter(
                vacationcard_id__in=vcard_ids, user_id=user_id)
            if vacation_card:
                vacation_card.delete()
                vacationtrip_info.delete()
                if businesscardvacation_info:
                    businesscardvacation_info.delete()
                return CustomeResponse(
                    {
                        'msg': 'Vacation card deleted successfully'
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    {'msg': 'Vacation card id not found'},
                    status=status.HTTP_201_CREATED
                )
        except Exception:
            logger.critical(
                "Caught exception in {0}".format(__file__),
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
        """Update vacation trips."""
        user_id = request.user

        if call_from_func:
            # Call from offline app
            try:
                vacation_id = offline_data['vcard_id']
                stops = offline_data['vacation_trips']
                vacation_name = offline_data['vacation_name']
                data = offline_data

            except KeyError:

                return CustomeResponse(
                    {
                        'msg': 'Vacation id not found'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        else:
            try:
                vacation_id = pk
                stops = request.data['vacation_trips']
                vacation_name = request.data['vacation_name']
                data = request.data
            except KeyError:
                return CustomeResponse(
                    {
                        'msg': 'Vacation id not found'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )

        try:
            vacationtrip = VacationTrip.objects.filter(
                vacationcard_id=vacation_id, user_id=user_id)

            if vacationtrip and vacation_name:

                tempContainer = []

                for data in stops:
                    tempdata = {}
                    tempdata = data
                    tempdata['vacationcard_id'] = vacation_id
                    tempContainer.append(tempdata)

                serializer = VacationEditTripSerializer(
                    data=tempContainer, many=True, context={'local_date': 1})

                if serializer.is_valid():
                    VacationCard.objects.filter(id=vacation_id).update(
                        vacation_name=vacation_name)
                    vacationtrip.delete()
                    serializer.save(user_id=request.user)

                    return CustomeResponse(
                        serializer.data, status=status.HTTP_200_OK)

                else:
                    #
                    return CustomeResponse(
                        {
                            "msg": "data is in wrong format check \
                            details once again"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)
            else:

                return CustomeResponse(
                    {
                        'msg': 'trip not found'
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
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

    def destroy(self, request, pk=None):
        """Delete vacation trip."""
        try:
            vacation_stop = VacationTrip.objects.filter(id=pk)

            if vacation_stop:
                vacationcard_id = vacation_stop[0].vacationcard_id
                vacation_id = vacationcard_id.id
                vacation_data = VacationTrip.objects.filter(
                    vacationcard_id=vacation_id)
                vacationcard_data = VacationCard.objects.filter(id=vacation_id)
                businesscard_vacation = BusinessCardVacation.objects.filter(
                    vacationcard_id=vacation_id)
                totalvacationdata = vacation_data.count()

                if totalvacationdata != 1:
                    vacation_stop.delete()
                    return CustomeResponse(
                        {
                            'msg': 'Trip has been deleted'
                        },
                        status=status.HTTP_200_OK
                    )

                if totalvacationdata == 1:
                    vacation_stop.delete()
                    vacationcard_data.delete()
                    if businesscard_vacation:
                        businesscard_vacation.delete()
                return CustomeResponse(
                    {
                        'msg': 'Trip and vacation card  has been deleted as you \
                        have only one stop in your vacation.'
                    },
                    status=status.HTTP_200_OK
                )

            else:
                return CustomeResponse(
                    {
                        'msg': 'Trip_id not found'
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


class BusinessCardVacationViewSet(viewsets.ModelViewSet):
    """Business card vacation views."""

    queryset = BusinessCardVacation.objects.select_related().all()
    serializer_class = BusinessCardVacationSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):

        try:
            vacation_id = self.request.query_params.get(
                'vacationcard_id',
                None
            )
            user_id = request.user.id
            queryset = VacationCard.objects.select_related(
            ).all().filter(user_id=user_id, id=vacation_id)
            serializer = SingleVacationCardSerializer(
                queryset,
                many=True
            )
            return CustomeResponse(
                serializer.data,
                status=status.HTTP_200_OK
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

    def create(self, request):
        """link business cards to vacation cards."""
        try:
            user_id = request.user.id

            # Apply Multiple Business Card to Multiple Vacation Card
            business_id = request.data['businesscard_id']
            vacation_id = request.data['vacationcard_id']

            count = 0
            for b_id in business_id:

                i = 0
                for v_id in vacation_id:

                    business_id[count]
                    businesscard_vacation = BusinessCardVacation.objects.filter(
                        businesscard_id=business_id[count], vacationcard_id=vacation_id[i])
                    if businesscard_vacation:
                        pass
                    else:
                        user_id = request.user.id
                        businessvacationcardserializer = BusinessCardVacationSerializer(
                            data=request.data, context={'request': request})
                        request.data['user_id'] = user_id
                        request.data['businesscard_id'] = business_id[count]
                        request.data['vacationcard_id'] = vacation_id[i]
                        if businessvacationcardserializer.is_valid():
                            businessvacationcardserializer.save()
                        else:
                            return CustomeResponse(
                                businessvacationcardserializer.errors,
                                status=status.HTTP_400_BAD_REQUEST,
                                validate_errors=1
                            )

                    i = i + 1

                count = count + 1

            return CustomeResponse(
                {
                    "msg": "Vacation Card has been applied successfully"
                },
                status=status.HTTP_201_CREATED
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
    def delete(self, request):
        """UnApply(Delete) multiple Businesscard to Vacation card."""
        try:
            user_id = request.user.id

            vcard_id = request.data['vacationcard_id']
            bcard_id = request.data['businesscard_id']

            businesscardinfo = BusinessCardVacation.objects.filter(
                vacationcard_id=vcard_id,
                businesscard_id__in=bcard_id,
                user_id=user_id
            )
            if businesscardinfo:
                businesscardinfo.delete()
                return CustomeResponse(
                    {
                        'msg': 'Business card has sucessfully unapply to \
                        vacation card'
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    {'msg': 'Id not found Bad request'},
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


class VacationCardMerge(APIView):
    """Vacation card merge."""
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
            merge vaction cards to one vacation card and delete all of\
            thems once done.
            accept from and list of arrays vacation card ids
        """
        try:

            serializer = VacationCardMergeSerializer(data=request.data)
            if serializer.is_valid():
                sourceVacationCardIds = request.data.get('source')
                destVacationCardId = request.data.get('dest')
                vacationCardIds = sourceVacationCardIds[:]
                vacationCardIds.append(destVacationCardId)

                vacationCardCount = VacationCard.objects.filter(
                    user_id=request.user, id__in=vacationCardIds).count()

                # ids must be belongs to session user and not dest id not in
                # source
                if vacationCardCount != len(vacationCardIds):
                    return CustomeResponse(
                        {
                            'msg': 'one or all of the vacation ids not exists'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # update source vacation card ids to destination vacation card
                # id
                VacationTrip.objects.filter(
                    user_id=request.user,
                    vacationcard_id__in=sourceVacationCardIds).update(
                    vacationcard_id=destVacationCardId)
                BusinessCardVacation.objects.filter(
                    user_id=request.user,
                    vacationcard_id__in=sourceVacationCardIds).update(
                    vacationcard_id=destVacationCardId)

                # remove source vacation card once it trips done
                VacationCard.objects.filter(
                    user_id=request.user,
                    id__in=sourceVacationCardIds).delete()

                vacationmerge_data = VacationTrip.objects.filter(
                    user_id=request.user, vacationcard_id=destVacationCardId)
                serializer = VacationDuplicateSerializer(
                    vacationmerge_data, many=True)
                return CustomeResponse(
                    serializer.data, status=status.HTTP_200_OK)
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
