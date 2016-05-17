# Standard library Imports
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status
from logging import getLogger
from django.conf import settings

# Third Party Imports
import boto3

# Local app imports
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
from models import AwsDeviceToken

import ohmgear.settings.aws as aws

logger = getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)


class AwsActivity(viewsets.ModelViewSet):

    queryset = AwsDeviceToken.objects.all()
    serializer_class = None
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return CustomeResponse({'msg': "GET METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def create(self, request):
        return CustomeResponse({'msg': "POST METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def destroy(self, request, pk=None):
        return CustomeResponse({'msg': "DELETE METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    @list_route(methods=['post'],)
    def register_to_aws(self, request):
        user_id = request.user
        try:
            device_token = request.data['device_token']
            device_type = request.data['device_type'].lower()
        except Exception as e:
            logger.error("Caught Exception in {}, {}".format(__file__, e))
            ravenclient.captureException()

            return CustomeResponse(
                {'msg': "Please provide device_token,device_type"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        if device_type == 'apns':
            platform_application_arn = aws.AWS_PLATEFORM_APPLICATION_ARN[
                "APNS"]
        elif device_type == 'gcm':
            platform_application_arn = aws.AWS_PLATEFORM_APPLICATION_ARN["GCM"]
        else:
            return CustomeResponse(
                {'msg': "device_type must be apns or gcm"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        if device_token and user_id and device_type:
            try:

                client = boto3.client('sns', **aws.AWS_CREDENTIAL)

                # TODO Need to check device token already exist or not
                # End
                # try:
                response = client.create_platform_endpoint(
                    PlatformApplicationArn=platform_application_arn,
                    Token=device_token,
                    CustomUserData='',
                    Attributes={}
                )

                if "EndpointArn" in response:
                    AwsDeviceToken.objects.update_or_create(
                        device_token=device_token,
                        aws_plateform_endpoint_arn=response["EndpointArn"],
                        user_id=user_id,
                        device_type=device_type
                    )

                return CustomeResponse(response, status=status.HTTP_200_OK)

            except Exception as e:
                logger.critical(
                    "Caught Exception in {}, {}".format(
                        __file__, e))
                ravenclient.captureException()

        else:
            return CustomeResponse(
                {
                    'msg': "Please provide device_token,device_type \
                    and user token"
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
