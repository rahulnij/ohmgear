from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import VacationTrip,BusinessCardVacation
from serializer import VacationTripSerializer,VacationCardSerializer,BusinessCardVacationSerializer
from ohmgear.functions import CustomeResponse
from rest_framework.decorators import api_view
import rest_framework.status as status
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json

class VacationCardViewSet(viewsets.ModelViewSet):
    queryset = VacationTrip.objects.select_related().all()
    serializer_class = VacationTripSerializer
    
    #--------------Method: GET-----------------------------#       
    def list(self,request):
        return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
    
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
         return CustomeResponse({'msg':'Stops added are not valid'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
     
     

class BusinessCardVacationViewSet(viewsets.ModelViewSet):
    
    queryset = BusinessCardVacation.objects.select_related().all()
    serializer_class    =   BusinessCardVacationSerializer
    
    def create(self,request):
        
        businesscardvacationserializer =    BusinessCardVacationSerializer(data=request.data,context ={'request':request})
        mutable = request.POST._mutable
        request.POST._mutable = True
       
        #print businesscard_id
        
        
        try:
            businesscard_id =  request.data['businesscard_id']
            bcard_id = json.loads(request.DATA['businesscard_id'])
            noofbusinesscard =  len(businesscard_id)
            vacationcard_id =  request.data['vacationcard_id'] 
            user_id =  request.data['user_id'] 

            tempContainer = []
            count = 0
            for data in bcard_id:
                tempdata = {"vacationcard_id":vacationcard_id,"businesscard_id":bcard_id[count],"user_id":user_id}
                tempContainer.append(tempdata)
                count = count+1
            serializer = BusinessCardVacationSerializer(data=tempContainer,many=True)
            if serializer.is_valid():        
                    serializer.save()
                    return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)
        except:
            return CustomeResponse({'status':'fail','msg':'Please provide all the credentials properly'},status=status.HTTP_400_BAD_REQUEST)
        
        
        