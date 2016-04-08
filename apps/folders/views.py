from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
import rest_framework.status as status

# Folder modules
from apps.folders.models import Folder, FolderContact
from apps.folders.serializer import FolderSerializer, FolderContactSerializer

# Authentication modules
from rest_framework.permissions import IsAuthenticated
from ohmgear.token_authentication import ExpiringTokenAuthentication
from permissions import IsUserData
from rest_framework.decorators import list_route


from ohmgear.functions import CustomeResponse
# create user and admin viewset or model


class CheckAccess(viewsets.ModelViewSet):
    permission_classes = (IsUserData, IsAuthenticated, )
    authentication_classes = (ExpiringTokenAuthentication,)

    def get_queryset(self):
        queryset = super(CheckAccess, self).get_queryset()
        user = self.request.user
        if user.user_type == 1:
            return queryset
        else:
            return queryset.filter(user_id=user)


class FolderViewSet(CheckAccess):

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsUserData, IsAuthenticated, )
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def get_queryset(self):
        queryset = super(FolderViewSet, self).get_queryset()
        #user = self.request.user
        return queryset

    def create(self, request, offline_data=None):
        if offline_data:
            folderSerializer = FolderSerializer(
                data=offline_data, context={'request': request})
        else:
            folderSerializer = FolderSerializer(
                data=request.data, context={'request': request})
        if folderSerializer.is_valid():
            folderSerializer.save(user_id=request.user)
            return CustomeResponse(folderSerializer.data, status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(folderSerializer.errors, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def update(self, request, pk=None):
        folder = get_object_or_404(self.get_queryset(), pk=pk)
        folderSerializer = FolderSerializer(folder, data=request.data)
        if folderSerializer.is_valid():
            folderSerializer.save()
            return CustomeResponse(folderSerializer.data, status=status.HTTP_201_CREATED)
        else:

            return CustomeResponse(folderSerializer.errors, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    @list_route(methods=['post'],)
    def folder_contact_link(self, request):

        folder_contact_serializer = FolderContactSerializer(
            data=request.data, context={'request': request})

        if folder_contact_serializer.is_valid():
            folder_contact_serializer.save(user_id=request.user)
            return CustomeResponse(folder_contact_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(folder_contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

#	def list(self, request):
#		queryset = self.get_queryset().all()
#		if not queryset:
#			return Response({'data not found'},status=status.HTTP_404_NOT_FOUND)
#		else:
#			folderSerializer = FolderSerializer(queryset,many=True)
#			print queryset.values()
#			return Response(folderSerializer.data)

    # def retrieve(self, request, pk=None):

    # 	folder = self.get_object(self.get_queryset(), pk=pk)
    # 	folderSerializer =  FolderSerializer(folder)
    # 	return Response(folderSerializer.data)

    # def delete(self, request, pk=None):

    # 	folder = get_object_or_404(self.get_queryset(), pk=pk)
    # 	# if folder has contacts then user can not able to delete the folder

    # 	folder.delete()
    # 	return Response(status=status.HTTP_200_OK)
