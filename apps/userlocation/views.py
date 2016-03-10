from rest_framework import viewsets
from rest_framework.decorators import list_route

from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from models import UserLocation
from apps.users.models import Profile


from ohmgear.settings.constant import REGION

from serializer import UserLocationSerializer
from apps.users.serializer import ProfileSerializer

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
		try:
			ul = self.queryset.get(user_id=request.user.id, region=REGION)
			geo1 = {"lat": ul.lat, "lon": ul.lon}
			
			uls = self.queryset.exclude(user_id=request.user.id, region=REGION)
			userIds = []
			for oul in uls:
				geo2 = {"lat": oul.lat, "lon": oul.lon}
				
				if self.locationWithin(geo1, geo2):
					userIds.append(oul.user_id)
				
			userProfiles = Profile.objects.filter(user_id__in=userIds)
			pserializer = ProfileSerializer(userProfiles, many=True)
				
			return CustomeResponse(pserializer.data,status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return CustomeResponse({"msg": "user current location not found"},status=status.HTTP_200_OK)

	def locationWithin(self, geo1, geo2, radius=200):
		from math import sin, cos, sqrt, atan2, radians
		# approximate radius of earth in km
		R = 6373.0
		
		lat1 = radians(geo1["lat"])
		lon1 = radians(geo1["lon"])
		lat2 = radians(geo2["lat"])
		lon2 = radians(geo2["lon"])
		dlon = lon2 - lon1
		dlat = lat2 - lat1

		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		#distance in meter
		distance = R * c * 1000
		print distance
		if distance <= radius:
			return True

		return False

		
