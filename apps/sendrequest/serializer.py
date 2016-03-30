from rest_framework import serializers
from models import Notification
# Serializers define the API representation.

        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification