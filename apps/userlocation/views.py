from rest_framework import viewsets
from rest_framework.decorators import list_route
import rest_framework.status as status
from django.db.models import Q
from django.contrib.gis.measure import D 
import datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from rest_framework.permissions import IsAuthenticated

from ohmgear.token_authentication import ExpiringTokenAuthentication

from models import UserLocation
from apps.users.models import Profile
from serializer import UserLocationSerializer
from apps.users.serializer import ProfileSerializer

from ohmgear.settings.constant import REGION

from ohmgear.functions import CustomeResponse


class UserLocationViewSet(viewsets.ModelViewSet):

	queryset = UserLocation.objects.all()
	serializer_class = UserLocationSerializer
	authentication_classes = (ExpiringTokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	
	def create(self, request):
		data = {}
		try:
			
			data['geom'] = 'POINT(%s %s)'%(request.data['lon'], request.data['lat'])

			ul = self.queryset.get(user_id=request.user.id, region=REGION)
			ulserializer = UserLocationSerializer(ul, data=data, partial=True)
		except MultipleObjectsReturned:
			pass
		except ObjectDoesNotExist:
			data['user_id'] = request.user.id
			data['region'] = REGION
			ulserializer = UserLocationSerializer(data=data)
			
			
		if ulserializer.is_valid():
			ulserializer.save()
			return CustomeResponse({"msg": "success"},status=status.HTTP_200_OK)
		
		print ulserializer.errors
		
		return CustomeResponse({"msg": "failed"},status=status.HTTP_200_OK)
		

	@list_route(methods=['GET'])
	def nearuser(self, request):
		try:
			radius = 100; # in meter
			ul = self.queryset.get(user_id=request.user.id, region=REGION)
			currentUserLocation = 'POINT(%s %s)'%(ul.geom.x, ul.geom.y)#{"lat": ul.lat, "lon": ul.lon}
			curTime = datetime.datetime.now()
			timeSubtract = datetime.timedelta(hours=1)
			timeBeforeCurrentTime = curTime - timeSubtract

			uls = self.queryset.filter(geom__distance_lte=(currentUserLocation, D(m=radius))).filter(~Q(id=ul.id)).filter(updated_date__gte=timeBeforeCurrentTime.strftime('%Y-%m-%d %H:%M:%S'))
			
			userIds = [oul.user_id for oul in uls]
				
			userProfiles = Profile.objects.filter(user_id__in=userIds)
			pserializer = ProfileSerializer(userProfiles, many=True, fields=('user', 'first_name','last_name', 'email'))
			
			return CustomeResponse(pserializer.data,status=status.HTTP_200_OK)
		except ObjectDoesNotExist:
			return CustomeResponse({"msg": "user current location not found"},status=status.HTTP_200_OK)

	

		
