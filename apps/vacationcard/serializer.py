from django.conf.urls import url, include
#from apps.identifiers.models import Identifier
from models import VacationTrip,VacationCard
from apps.businesscards.models import BusinessCardVacation
from rest_framework import routers, serializers, viewsets
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
            
            
class VacationTripSerializer(serializers.ModelSerializer):
    
    startdate = []
    enddate  = []
    class Meta:
        model = VacationTrip                
        fields = (
            'id',
            'vacation_type',
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
        
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        
        self.startdate.append(str(data['trip_start_date']))
        
        self.enddate.append(str(data['trip_end_date']))
        
        
        format = {'start_date':self.startdate,'end_date':self.enddate}
        #print format
        if data['trip_start_date'] > data['trip_end_date']:
            raise serializers.ValidationError("finish must occur after start")
        
    
        return data
        
        

class VacationCardSerializer(serializers.ModelSerializer):
    attached_business_cards = serializers.IntegerField(source='businesscardvacation.count',read_only=True)
    vacation_trips = VacationTripSerializer(many=True,read_only=True)
    class Meta:
        model = VacationCard
        fields = ('id','user_id','vacation_name','vacation_trips','attached_business_cards')

class VacationCardMergeSerializer(serializers.Serializer):
    dest = serializers.IntegerField(required=True)
    source = serializers.ListField(child=serializers.IntegerField(required=True))
        
class BusinessCardVacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCardVacation
        fields = (
            'id',
            'vacationcard_id',
            'businesscard_id',
            'user_id'
        )