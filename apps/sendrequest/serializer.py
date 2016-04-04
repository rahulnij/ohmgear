from rest_framework import serializers
from models import SendRequest
# Serializers define the API representation.

        
class SendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendRequest