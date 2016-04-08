import rest_framework.status as status
from rest_framework import viewsets

from models import Notes
from serializer import NotesSerializer
from ohmgear.functions import CustomeResponse


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Notes.objects.select_related().all()
    serializer_class = NotesSerializer

    def list(self, request):
        return CustomeResponse({'msg': 'GET method not allowed'},
                               status=status.HTTP_405_METHOD_NOT_ALLOWED,
                               validate_errors=1)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        notes = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(notes, context={'request': request})

        return CustomeResponse(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        pass

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return CustomeResponse({}, status=status.HTTP_200_OK)
