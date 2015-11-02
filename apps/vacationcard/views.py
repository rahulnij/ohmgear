from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import VacationTrip
from serializer import VacationTripSerializer,VacationCardSerializer
from ohmgear.functions import CustomeResponse
from rest_framework.decorators import api_view
import rest_framework.status as status
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json

class VacationCardViewSet(viewsets.ModelViewSet):
    queryset = VacationTrip.objects.select_related().all()
    serializer_class = VacationTripSerializer
    
    def create(self,request):
        
        VacationCardserializer = VacationCardSerializer(data=request.DATA,context={'request':request})
        VacationTripserializer = VacationTripSerializer(data=request.DATA,context={'request':request})
        vacation = request.DATA['vacation']
        user_id    =   request.DATA['user_id']
        
        try:
             stops = json.loads(request.DATA['vacation'])
        except:
            return CustomeResponse({'status':'fail','msg':'Please provide correct Json Format'},status=status.HTTP_400_BAD_REQUEST)
            
        
        if VacationCardserializer.is_valid():
            vacationid = VacationCardserializer.save()  
            
        if stops:
                tempContainer = []
                for data in stops:
                    tempdata = {}
                    tempdata =   data
                    tempdata['vacationcard_id'] = vacationid.id
                    tempContainer.append(tempdata)
                    
                serializer = VacationTripSerializer(data=tempContainer,many=True)
                if serializer.is_valid():
                    serializer.save()
                    return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
                else:
                 return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)
        else:
         return CustomeResponse({'msg':'Please provide operation parameter op'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
        