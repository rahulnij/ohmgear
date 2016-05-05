"""Notes view set."""

import rest_framework.status as status
from rest_framework import viewsets
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404
import logging

from models import Notes
from serializer import NotesSerializer
from ohmgear.functions import CustomeResponse

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)


class NotesViewSet(viewsets.ModelViewSet):
    """Notes views."""

    queryset = Notes.objects.select_related().all()
    serializer_class = NotesSerializer

    def list(self, request):
        """Listing not allowed."""
        return CustomeResponse({'msg': 'GET method not allowed'},
                               status=status.HTTP_405_METHOD_NOT_ALLOWED,
                               validate_errors=1)

    def retrieve(self, request, pk=None):
        """Get note by pk."""
        try:
            try:
                queryset = self.queryset
                notes = get_object_or_404(queryset, pk=pk)
                serializer = self.serializer_class(
                    notes, context={'request': request})

                return CustomeResponse(
                    serializer.data, status=status.HTTP_200_OK)
            except Http404:
                logger.error(
                    "Caught Http404(DoesNotExist) exception for {}, primary key {},\
                    in {}".format(
                        Notes.__name__, pk, __file__
                    )
                )
                return CustomeResponse(
                    {
                        "msg": "Notes does not exist."
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

    def partial_update(self, request, pk=None):
        """Not implement."""
        pass

    def delete(self, request, pk, format=None):
        """Delete note."""
        try:
            snippet = self.get_object(pk)
            snippet.delete()
            return CustomeResponse({}, status=status.HTTP_200_OK)
        except Notes.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, node id {}, \
                in {}".format(
                    Notes.__name__, pk, __file__
                )
            )
            return CustomeResponse(
                {
                    "msg": "Notes does not exist."
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
