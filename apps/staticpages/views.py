from rest_framework import viewsets
import rest_framework.status as status

from ohmgear.functions import CustomeResponse
from models import StaticPages
from serializer import StaticPagesSerializer


class StaticPagesViewSet(viewsets.ModelViewSet):
    queryset = StaticPages.objects.all()
    serializer_class = StaticPagesSerializer

    def list(self, request):

        page_name = self.request.QUERY_PARAMS.get('page_name', None)

        if page_name is not None:
            queryset = StaticPages.objects.get(page_name=page_name)

        if queryset:
            serializer = StaticPagesSerializer(queryset)
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {"msg": "data not found"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
