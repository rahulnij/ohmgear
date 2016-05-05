"""user location view."""

# Import Python Modules
import datetime
# Third Party Imports
from django.contrib.gis.measure import D
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status
from django.conf import settings
import logging

# Local app imports
from models import UserLocation
from apps.users.models import Profile
from ohmgear.token_authentication import ExpiringTokenAuthentication
from serializer import UserLocationSerializer
from .serializer import ProfileWithConnectionStatusSerializer
from ohmgear.settings.constant import REGION
from ohmgear.functions import CustomeResponse
from ohmgear.settings.constant import RADAR_RADIUS

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)


class UserLocationViewSet(viewsets.ModelViewSet):
    """Store user geography location and get user list near by to a user."""

    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """Insert user current location and store one only one location."""
        data = {}
        try:
            try:
                user_id = request.user.id
                data['geom'] = 'POINT(%s %s)' % (
                    request.data['lon'],
                    request.data['lat']
                )

                ul = self.queryset.get(user_id=user_id, region=REGION)
                ulserializer = UserLocationSerializer(
                    ul,
                    data=data,
                    partial=True
                )
            except UserLocation.MultipleObjectsReturned:
                logger.error(
                    "Caught MultipleObjectsReturned exception for {}, user_id {},\
                    in {}".format(
                        UserLocation.__name__, user_id, __file__
                    )
                )
                ravenclient.captureException()
            except UserLocation.DoesNotExist:
                data['user_id'] = user_id
                data['region'] = REGION
                ulserializer = UserLocationSerializer(data=data)

            if ulserializer.is_valid():
                ulserializer.save()
                return CustomeResponse({}, status=status.HTTP_204_NO_CONTENT)

            return CustomeResponse(
                ulserializer.errors,
                status=status.HTTP_400_BAD_REQUEST
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

    @list_route(methods=['GET'])
    def nearuser(self, request):
        """Return near by users."""
        try:
            radius = RADAR_RADIUS  # in meter
            user_id = request.user.id
            ul = self.queryset.get(user_id=user_id, region=REGION)
            current_user_location = 'POINT(%s %s)' % (
                ul.geom.x,  # latigude
                ul.geom.y  # logitude
            )
            currrent_datetime = datetime.datetime.utcnow()
            time_subtract = datetime.timedelta(minutes=30)
            currrent_datetime_after_subtract = currrent_datetime - time_subtract

            uls = self.queryset.filter(
                geom__distance_lte=(
                    current_user_location,
                    D(m=radius)
                )
            ).filter(
                ~Q(id=ul.id)
            ).filter(
                updated_date__gte=currrent_datetime_after_subtract.
                strftime('%Y-%m-%d %H:%M:%S')
            )

            user_ids = [oul.user_id for oul in uls]

            user_profiles = Profile.objects.filter(user_id__in=user_ids)

            pserializer = ProfileWithConnectionStatusSerializer(
                user_profiles,
                many=True, fields=(
                    'user',
                    'first_name',
                    'last_name',
                    'email',
                    'profile_image',
                    'defaultbusinesscard_id',
                    'is_connected'
                ), context={"connected_user_id": user_id}

            )

            return CustomeResponse(pserializer.data, status=status.HTTP_200_OK)
        except UserLocation.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, user_id {},\
                in {}".format(
                    UserLocation.__name, user_id, __file__
                )
            )
            return CustomeResponse(
                {
                    "msg": "Current user location unknow."
                },
                status=status.HTTP_404_NOT_FOUND
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
