from django.conf.urls import url, include
from models import Feedbacks
from rest_framework import routers, serializers, viewsets
            
class FeedbacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
            