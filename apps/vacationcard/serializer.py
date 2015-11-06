from django.conf.urls import url, include
#from apps.identifiers.models import Identifier
from models import VacationTrip,VacationCard
from apps.businesscards.models import BusinessCardVacation
from rest_framework import routers, serializers, viewsets
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
            
            
class VacationTripSerializer(serializers.ModelSerializer):

    class Meta:
        model = VacationTrip
        fields = (
            'id',
            'country',
            'state',
            'city',
            'contact_no',
            'notes',
            'trip_start_date',
            'trip_end_date',
            'user_id',
            'vacationcard_id'
        )
        
        

class VacationCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacationCard
        fields = ('id','user_id',)
        
class BusinessCardVacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCardVacation
        fields = (
            'id',
            'vacationcard_id',
            'businesscard_id',
            'user_id'
        )