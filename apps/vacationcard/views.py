from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import VacationTrip,BusinessCardVacation,VacationCard
from serializer import VacationTripSerializer,VacationCardSerializer,BusinessCardVacationSerializer
from ohmgear.functions import CustomeResponse
from rest_framework.decorators import api_view
import rest_framework.status as status
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import itertools
from django.db.models import Count,Min, Max

class VacationCardViewSet(viewsets.ModelViewSet):
    queryset = VacationTrip.objects.select_related().all()
    #serializer_class = VacationTripSerializer
    serializer_class = VacationCardSerializer
    #--------------Method: GET-----------------------------#       
    def list(self,request):
        if request.method == 'GET':
           # user = user_profile.user
            user_id =   self.request.QUERY_PARAMS.get('user_id',None)
            Uservacationcardinfo = VacationCard.objects.filter(user_id=user_id).values()
            totalvacationcard =  Uservacationcardinfo.count()
            uservacationcard = []
            for i in range(totalvacationcard):
                
                vacationcardid =   Uservacationcardinfo[i]['id']
                uservacationcard.append(vacationcardid)
            userbusinessvacationcardinfo = BusinessCardVacation.objects.values('vacationcard_id').annotate(totalnoofbusinesscard=Count('businesscard_id')).filter(vacationcard_id__in = uservacationcard)

            uservacationtripinfo = VacationTrip.objects.values('vacationcard_id','country','state').annotate(min_start_date=Min('trip_start_date'),max_end_date = Max('trip_end_date')).filter(vacationcard_id__in = uservacationcard)
                
                
            lst = sorted(itertools.chain(userbusinessvacationcardinfo,uservacationtripinfo), key=lambda x:x['vacationcard_id'])
            list_c = []
            for k,v in itertools.groupby(lst, key=lambda x:x['vacationcard_id']):
                d = {}
                for dct in v:
                    d.update(dct)
                list_c.append(d)
            #print list_c
            if list_c:
                return CustomeResponse({'msg':list_c},status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse({'msg':"No Data Found"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                
    def create(self,request):
        
        VacationCardserializer = VacationCardSerializer(data=request.DATA,context={'request':request})
        VacationTripserializer = VacationTripSerializer(data=request.DATA,context={'request':request})
      
        try:
            vacation = request.DATA['vacation']
            stops = json.loads(request.DATA['vacation'])
            stops =  stops["data"]
        except:
            return CustomeResponse({'status':'fail','msg':'Please provide correct Json Format of vacation'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
        if VacationCardserializer.is_valid():
            vacationid = VacationCardserializer.save()
            if stops and vacationid.id:
                    tempContainer = []
                    for data in stops:
                        temp_dict = u''
                        tempdata = {}
                        #tempdata =   data
                        tempdata["x"] =   data
                        #stops += data
                        tempdata["x"]['vacationcard_id'] = vacationid.id
                        #tempdata['vacationcard_id'] = vacationid.id
                        tempContainer.append(tempdata)
                    
                     
                        tempContainer =  tempContainer[0]['x']
                    

                    serializer = VacationTripSerializer(data=[tempContainer],many=True)
                    if serializer.is_valid():
                        serializer.save()
                        return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
                    else:
                     return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)
        else:
         return CustomeResponse(VacationCardserializer.errors,status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
     
     

class BusinessCardVacationViewSet(viewsets.ModelViewSet):
    
    queryset = BusinessCardVacation.objects.select_related().all()
    serializer_class    =   BusinessCardVacationSerializer
    
    def list(self,request):
        
        
        return CustomeResponse({'msg':'Get Method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
    
    def create(self,request):
        
        serializer =    BusinessCardVacationSerializer(data=request.data,context ={'request':request})
        mutable = request.POST._mutable
        request.POST._mutable = True 
        
        try:
            businesscard_id =  request.data['businesscard_id']
            bcard_id = json.loads(request.DATA['businesscard_id'])
        except:
            return CustomeResponse({'status':'fail','msg':'Please provide businesscard_id'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        request.DATA['businesscard_id'] = bcard_id[0]  
        
        if serializer.is_valid(): 
            vacationcard_id =  request.data['vacationcard_id'] 
            user_id =  request.data['user_id'] 
            tempContainer = []
            count = 0
            for data in bcard_id:
                tempdata = {"vacationcard_id":vacationcard_id,"businesscard_id":bcard_id[count],"user_id":user_id}
                tempContainer.append(tempdata)
                count = count+1
            businessvacationcardserializer = BusinessCardVacationSerializer(data=tempContainer,many=True)    
            if businessvacationcardserializer.is_valid(): 
                businessvacationcardserializer.save()
                return CustomeResponse(businessvacationcardserializer.data,status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(businessvacationcardserializer.errors,status=status.HTTP_201_CREATED,validate_errors=1)
        else:
                return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED,validate_errors=1)

        
        
        