# Third Party Imports
from rest_framework import serializers

# Local app imports
from models import UserLocation


class UserLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserLocation
