from rest_framework import viewsets
from rest_framework.decorators import list_route

from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from models import UserLocation

from ohmgear.settings.constant import REGION

from serializer import UserLocationSerializer

from ohmgear.functions import CustomeResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import rest_framework.status as status
class UserLocationViewSet(viewsets.ModelViewSet):

	queryset = UserLocation.objects.all()
	serializer_class = UserLocationSerializer
	authentication_classes = (ExpiringTokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	
	def create(self, request):
		data = {}
		try:
			data['user_id'] = request.user.id
			data['region'] = REGION
			data['lat'] = request.data['lat']
			data['lon'] = request.data['lon']
			
			ul = self.queryset.get(user_id=request.user.id, region=REGION)
			ulserializer = UserLocationSerializer(ul, data=request.data, partial=True)
		except MultipleObjectsReturned:
			pass
		except ObjectDoesNotExist:
			ulserializer = UserLocationSerializer(data=data)
				
		
		
		if ulserializer.is_valid():
			ulserializer.save()
			return CustomeResponse({"msg": "success"},status=status.HTTP_200_OK)
		
		print ulserializer.errors
		
		return CustomeResponse({"msg": "failed"},status=status.HTTP_200_OK)
		

	@list_route(methods=['GET'])
	def nearuser(self, request):
		self.queryset.filter(user_id=request.user.id)


