"""Stagic page views."""

from rest_framework import viewsets
import rest_framework.status as status
from django.conf import settings
import logging

from ohmgear.functions import CustomeResponse
from models import StaticPages
from serializer import StaticPagesSerializer

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)


class StaticPagesViewSet(viewsets.ModelViewSet):
    """Staticpage viewset."""

    queryset = StaticPages.objects.all()
    serializer_class = StaticPagesSerializer

    def list(self, request):
        """Get page data."""
        try:
            page_name = self.request.data['page_name']

            queryset = StaticPages.objects.get(page_name=page_name)

            serializer = StaticPagesSerializer(queryset)
            return CustomeResponse(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except StaticPages.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, node id {}, \
                in {}".format(
                    StaticPages.__name__, page_name, __file__
                )
            )
            return CustomeResponse(
                {
                    "msg": "Data not found."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except StaticPages.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, node id {}, \
                in {}".format(
                    StaticPages.__name__, page_name, __file__
                )
            )
            return CustomeResponse(
                {"msg": "Data not found."},
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

    def create(self, request):
        """Create new static page."""
        try:
            data = self.request.data

            static_page_serializer = StaticPagesSerializer(data=data)

            if static_page_serializer.is_valid():
                return CustomeResponse(
                    static_page_serializer.data,
                    status=status.HTTP_200_OK)
            else:
                return CustomeResponse(
                    static_page_serializer.errors,
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
