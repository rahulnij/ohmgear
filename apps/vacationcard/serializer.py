from django.conf.urls import url, include
#from apps.identifiers.models import Identifier
from models import VacationTrip,VacationCard
from apps.businesscards.models import BusinessCardVacation
from rest_framework import routers, serializers, viewsets
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
from datetime import datetime

            
            
class VacationTripSerializer(serializers.ModelSerializer):
    
    local_date = []
    count = 0
    
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
        check = self.context.get("local_date")
        if check and self.count == 0:
           self.local_date = []
           self.count = 1
        start_time = datetime.strptime(str(data['trip_start_date']),'%Y-%m-%d')
        end_date = datetime.strptime(str(data['trip_end_date']),'%Y-%m-%d')
        if self.local_date:
            for tempData in self.local_date:
                if tempData['trip_start_date'] > start_time:
                    raise serializers.ValidationError("Start date must be greater than other stop start date")
                if tempData['trip_end_date'] > start_time:
                    raise serializers.ValidationError("Start date must be greater than other stop end date")
        
        if data['trip_start_date'] > data['trip_end_date']:
            raise serializers.ValidationError("End date must be greater then start date")
        
        format = {'trip_start_date':datetime.strptime(str(data['trip_start_date']),'%Y-%m-%d'),'trip_end_date':datetime.strptime(str(data['trip_end_date']),'%Y-%m-%d')}
        self.local_date.append(format)
        
        return data
    
    

        
        
class VacationEditTripSerializer(serializers.ModelSerializer):
    
    local_date = []
    count = 0

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
        check = self.context.get("local_date")
        if check and self.count == 0:
           self.local_date = []
           self.count = 1
        start_time = datetime.strptime(str(data['trip_start_date']),'%Y-%m-%d')
        end_date = datetime.strptime(str(data['trip_end_date']),'%Y-%m-%d')
        if self.local_date:
            for tempData in self.local_date:
                if tempData['trip_start_date'] > start_time:
                    raise serializers.ValidationError("Start date must be greater than other stop start date")
                if tempData['trip_end_date'] > start_time:
                    raise serializers.ValidationError("Start date must be greater than other stop end date")
        
        if data['trip_start_date'] > data['trip_end_date']:
            raise serializers.ValidationError("End date must be greater then start date")
        
        format = {'trip_start_date':datetime.strptime(str(data['trip_start_date']),'%Y-%m-%d'),'trip_end_date':datetime.strptime(str(data['trip_end_date']),'%Y-%m-%d')}
        self.local_date.append(format)
        
        return data
        


class VacationCardSerializer(serializers.ModelSerializer):
    attached_business_cards = serializers.IntegerField(source='businesscardvacation.count',read_only=True)
   # business_vacation = BusinessCardSerializer(many=True,read_only=True)
    vacation_trips = VacationTripSerializer(many=True,read_only=True)
    class Meta:
        model = VacationCard
        fields = ('id','user_id','vacation_name','vacation_trips','attached_business_cards','business_vacation')



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

from apps.businesscards.serializer import BusinessCardSerializer        
class SingleVacationCardSerializer(serializers.ModelSerializer):
    #vacationbusinesscard = BusinessCardVacationSerializer(many=True,read_only=True)
    business_vacation = BusinessCardSerializer(many=True,read_only=True)
    vacation_trips = VacationTripSerializer(many=True,read_only=True)
    class Meta:
        model = VacationCard
        fields = ('id','user_id','vacation_name','vacation_trips','business_vacation')        