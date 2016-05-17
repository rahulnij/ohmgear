
# django imports
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework import viewsets
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404


# third party imports
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
import datetime
import random
import logging

# application imports
from models import Identifier, LockIdentifier
from serializer import (
    IdentifierSerializer,
    LockIdentifierSerializer,
    BusinessIdentifierSerializer
)
from functions import CreateSystemIdentifier

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)


class IdentifierViewSet(viewsets.ModelViewSet):
    """Identifier View."""

    queryset = Identifier.objects.select_related().all()
    serializer_class = IdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, **kwargs):
        """
        TODO: need urgent optimization, performing more than one function.

        Get all user identifier.

        Also check if identifier exist give suggested identifier.
        """

        try:
            identifier = self.request.query_params.get('identifier', None)
            user = self.request.query_params.get('user', None)
        except KeyError:
            logger.error(
                "Caught KeyError exception: group_id \
            is required  , in {}".format(
                    __file__
                )
            )
            return CustomeResponse(
                {
                    'msg': 'key not found'
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        try:
            # check whether identifier is exist or not if not give suggested
            # identifier

            # Get all identifiers of the user
            userdata = Identifier.objects.select_related(
                'businesscard_identifiers').filter(user=user).order_by('-id')

            if userdata:
                serializer = BusinessIdentifierSerializer(
                    userdata, many=True)
                return CustomeResponse(
                    serializer.data, status=status.HTTP_201_CREATED)
            else:

                if identifier is None:
                    return CustomeResponse(
                        {
                            'msg': 'user id is not exist'
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )

                try:
                    Identifier.objects.get(
                        identifier=identifier
                    )
                    list = []
                    for i in range(5):
                        identifiersuggestion = ''.join(
                            random.choice('0123456789') for i in range(2))
                        newidentifier = identifier + identifiersuggestion
                        matchidentifier = Identifier.objects.get(
                            identifier=newidentifier)
                        if not matchidentifier:
                            list.append(newidentifier)
                    return CustomeResponse(
                        {"msg": list}, status=status.HTTP_200_OK,
                        validate_errors=True
                    )
                except Identifier.DoesNotExist:
                    # no need to log
                    return CustomeResponse(
                        {
                            'msg': 'Identifier available'
                        },
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

    def retrieve(self, request, pk=None):
        """Retrive identifier."""
        try:
            queryset = self.queryset
            identifier = get_object_or_404(queryset, pk=pk)
            serializer = self.serializer_class(
                identifier, context={'request': request})

            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            logger.error(
                "Caught Http404(DoesNotExist) exception for {}, primary key {},\
                in {}".format(
                    Identifier.__name__, pk, __file__
                )
            )
            return CustomeResponse(
                {
                    "msg": "Identifier does not exist."
                },
                status=status.HTTP_404_NOT_FOUND,
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

    def create(self, request):
        """Create new identifer for system generated or premium."""
        try:
            data = request.data.copy()
            data['user'] = request.user.id
            data['identifierlastdate'] = str(
                (datetime.date.today() + datetime.timedelta(3 * 365 / 12)).isoformat())

            serializer = IdentifierSerializer(
                data=data,
                context={'request': request, 'msg': 'not exist'}
            )
            identifier = data['identifier']
            if serializer.is_valid():
                serializer.save()
                try:
                    remove_lock_data = ''
                    remove_lock_data = LockIdentifier.objects.get(
                        identifier=identifier)
                except LockIdentifier.DoesNotExist:
                    logger.error(
                        "Caught DoesNotExist exception for {}, identifier {}, \
                        in {}".format(
                            LockIdentifier.__name__, identifier, __file__
                        )
                    )
                if remove_lock_data:
                    remove_lock_data.delete()
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(
                    serializer.errors,
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
    def refreshidentifier(self, request):
        """Refresh identifier will generate new identifier eveytime."""
        try:
            user_id = request.user
            if user_id:
                getidentifier = CreateSystemIdentifier()

                if getidentifier:
                    return CustomeResponse(
                        {
                            'identifier': getidentifier
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return CustomeResponse(
                        {
                            'msg': 'Identifier Not exist'
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
            else:
                return CustomeResponse(
                    {
                        'msg': 'Invalid User'
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
    def lockidentifier(self, request):
        """
        Lock identiifer will lock identifer for that user.

        If any other user request for it will not be given.
        """
        try:
            data = request.data.copy()
            data['user'] = request.user.id
            serializer = LockIdentifierSerializer(
                data=data, context={'request': data, 'msg': 'not exist'})
            identifier = data['identifier']
            if serializer.is_valid():

                try:
                    identifier_exist = ''
                    identifier_lock_exist = ''
                    identifier_exist = Identifier.objects.get(
                        identifier=identifier)
                    identifier_lock_exist = LockIdentifier.objects.get(
                        identifier=identifier)
                except Identifier.DoesNotExist:
                    logger.error(
                        "Caught DoesNotExist exception for {}, identifier {},\
                    in {}".format(
                            self.__class__, identifier, __file__
                        )
                    )
                except LockIdentifier.DoesNotExist:
                    logger.error(
                        "Caught DoesNotExist exception for {}, identifier {},\
                    in {}".format(
                            self.__class__, identifier, __file__
                        )
                    )
                if identifier_exist or identifier_lock_exist:
                    return CustomeResponse(
                        {'msg': 'Identifier is already locked'})
                else:
                    serializer.save()
                    return CustomeResponse(
                        serializer.data, status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(
                    {'msg': serializer.errors}, validate_errors=1)
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
