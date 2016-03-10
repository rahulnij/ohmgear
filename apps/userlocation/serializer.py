from rest_framework import serializers

from models import UserLocation

class UserLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserLocation
		