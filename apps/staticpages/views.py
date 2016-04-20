from rest_framework import viewsets
import rest_framework.status as status

from ohmgear.functions import CustomeResponse
from models import StaticPages
from serializer import StaticPagesSerializer


class StaticPagesViewSet(viewsets.ModelViewSet):
    queryset = StaticPages.objects.all()
    serializer_class = StaticPagesSerializer

    def list(self, request):

        page_name = self.request.query_params.get('page_name', None)

        if page_name is not None:
            queryset = StaticPages.objects.filter(page_name=page_name)

        if queryset:
            serializer = StaticPagesSerializer(queryset)
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {"msg": "data not found"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

    def create(self, request):
        data = self.request.data

        static_page_serializer = StaticPagesSerializer(data = data)

        if static_page_serializer.is_valid():
            return CustomeResponse(
                static_page_serializer.data,
                status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                static_page_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
