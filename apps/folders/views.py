# Django imports
from rest_framework.permissions import IsAuthenticated
from ohmgear.token_authentication import ExpiringTokenAuthentication
from permissions import IsUserData
from rest_framework.decorators import list_route
from django.shortcuts import get_object_or_404
from ohmgear.functions import CustomeResponse
from rest_framework import viewsets
import rest_framework.status as status
from django.conf import settings
import logging

# Application modules
from apps.folders.models import Folder
from apps.folders.serializer import FolderSerializer, FolderContactSerializer

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)


class CheckAccess(viewsets.ModelViewSet):
    permission_classes = (IsUserData, IsAuthenticated, )
    authentication_classes = (ExpiringTokenAuthentication,)

    def get_queryset(self):
        try:
            queryset = super(CheckAccess, self).get_queryset()
            user = self.request.user
            if user.user_type == 1:
                return queryset
            else:
                return queryset.filter(user_id=user)
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
        ravenclient.captureException()


class FolderViewSet(CheckAccess):

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsUserData, IsAuthenticated, )
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self):
        queryset = super(FolderViewSet, self).get_queryset()
        return queryset

    def create(self, request, offline_data=None):
        try:
            if offline_data:
                folder_serializer = FolderSerializer(
                    data=offline_data, context={'request': request})
            else:
                folder_serializer = FolderSerializer(
                    data=request.data, context={'request': request})
            if folder_serializer.is_valid():
                folder_serializer.save(user_id=request.user)
                return CustomeResponse(
                    folder_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    folder_serializer.errors,
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

    def update(self, request, pk=None):
        """Update folder data."""
        try:
            folder = get_object_or_404(self.get_queryset(), pk=pk)
            folder_serializer = FolderSerializer(folder, data=request.data)
            if folder_serializer.is_valid():
                folder_serializer.save()
                return CustomeResponse(
                    folder_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    folder_serializer.errors,
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

    def destroy(self, request, pk=None):
        """Delete folder not allowed on folder."""
        return CustomeResponse({'msg': 'Delete method not allowed'},
                               status=status.HTTP_405_METHOD_NOT_ALLOWED,
                               validate_errors=1)

    @list_route(methods=['post'],)
    def folder_contact_link(self, request):
        """Folder contact link."""
        try:
            folder_contact_serializer = FolderContactSerializer(
                data=request.data, context={'request': request})

            if folder_contact_serializer.is_valid():
                folder_contact_serializer.save(user_id=request.user)
                return CustomeResponse(
                    folder_contact_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return CustomeResponse(
                    folder_contact_serializer.errors,
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
