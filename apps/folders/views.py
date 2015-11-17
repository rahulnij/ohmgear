from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
import rest_framework.status as status

#Folder modules
from apps.folders.models import Folder
from apps.folders.serializer import FolderSerializer

#Authentication modules
from rest_framework.permissions import IsAuthenticated
from ohmgear.token_authentication import ExpiringTokenAuthentication

# create user and admin viewset or model


class FolderViewSet(viewsets.ViewSet):
	authentication_classes = (ExpiringTokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Folder.objects.all()

	def create(self, request):
			
		#request.data['user_id'] = 1
		#request.data['businesscard_id'] = 1
		#print request.data,'---'

		folderSerializer = FolderSerializer(data=request.data)
		if folderSerializer.is_valid():
			folderSerializer.save()
			return Response(folderSerializer.data,status=status.HTTP_201_CREATED)
		else:
			return Response(folderSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk=None):
		folder =get_object_or_404(self.queryset, pk=pk)
		folderSerializer = FolderSerializer(folder,data=request.data)
		if folderSerializer.is_valid():
			folderSerializer.save()
			return Response(folderSerializer.data,status=status.HTTP_201_CREATED)
		else:

			return Response(folderSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def list(self, request):
		queryset = Folder.objects.all()
		if not queryset:
			return Response({'data not found'},status=status.HTTP_404_NOT_FOUND)
		else:
			folderSerializer = FolderSerializer(queryset,many=True)
			print queryset.values()
			return Response(folderSerializer.data)

	def retrieve(self, request, pk=None):
		folder = get_object_or_404(self.queryset, pk=pk)
		folderSerializer =  FolderSerializer(folder)
		return Response(folderSerializer.data)


	def delete(self, request, pk=None):

		folder = get_object_or_404(self.queryset, pk=pk)
		# if folder has contacts then user can not able to delete the folder
		
		folder.delete()
		return Response(status=status.HTTP_200_OK)








