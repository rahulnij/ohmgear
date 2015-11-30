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
from permissions import IsUserData

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

	#authentication_classes = (ExpiringTokenAuthentication,)
	#permission_classes = (IsUserData, IsAuthenticated, )
	queryset = Folder.objects.all()
	serializer_class = FolderSerializer

 	def get_queryset(self):
	    queryset = super(FolderViewSet, self).get_queryset()
	    #user = self.request.user
	    return queryset

	# def create(self, request):
			
	# 	#request.data['user_id'] = 1
	# 	#request.data['businesscard_id'] = 1
		

	# 	folderSerializer = FolderSerializer(data=request.data, context={'request':request})
	# 	print request.data,' --- ', folderSerializer.is_valid()
	# 	if folderSerializer.is_valid():
	# 		folderSerializer.save(user_id=request.user)
	# 		return Response(folderSerializer.data,status=status.HTTP_201_CREATED)
	# 	else:
	# 		return Response(folderSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

	# def update(self, request, pk=None):
	# 	folder =get_object_or_404(self.get_queryset(), pk=pk)
	# 	folderSerializer = FolderSerializer(folder,data=request.data)
	# 	if folderSerializer.is_valid():
	# 		folderSerializer.save()
	# 		return Response(folderSerializer.data,status=status.HTTP_201_CREATED)
	# 	else:

	# 		return Response(folderSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def list(self, request):
		queryset = self.get_queryset().all()
		if not queryset:
			return Response({'data not found'},status=status.HTTP_404_NOT_FOUND)
		else:
			folderSerializer = FolderSerializer(queryset,many=True)
			print queryset.values()
			return Response(folderSerializer.data)

	# def retrieve(self, request, pk=None):
		
	# 	folder = self.get_object(self.get_queryset(), pk=pk)
	# 	folderSerializer =  FolderSerializer(folder)
	# 	return Response(folderSerializer.data)


	# def delete(self, request, pk=None):

	# 	folder = get_object_or_404(self.get_queryset(), pk=pk)
	# 	# if folder has contacts then user can not able to delete the folder
		
	# 	folder.delete()
	# 	return Response(status=status.HTTP_200_OK)









