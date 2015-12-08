from rest_framework import routers, serializers, viewsets
from models import VacationTrip,VacationCard
from serializer import VacationTripSerializer,VacationCardSerializer,BusinessCardVacationSerializer
from ohmgear.functions import CustomeResponse
from rest_framework.decorators import api_view
import rest_framework.status as status
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import itertools
from django.db.models import Count,Min, Max
from apps.businesscards.models import BusinessCardVacation,BusinessCard

from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from serializer import VacationCardMergeSerializer


class VacationCardViewSet(viewsets.ModelViewSet):
    queryset = VacationTrip.objects.select_related().all()
    #serializer_class = VacationTripSerializer
    serializer_class = VacationTripSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
    #--------------Method: GET-----------------------------#       
    def list(self,request):
        
        if request.method == 'GET':
           #-----------get all vacations of the user and no of business card attached to it------# 
           # user = user_profile.user
            user_id =  request.user.id
#            #print user_id
#            #user_id =   self.request.QUERY_PARAMS.get('user_id',None)
#            Uservacationcardinfo = VacationCard.objects.filter(user_id=user_id).values()
#            totalvacationcard =  Uservacationcardinfo.count()
#            uservacationcard = []
#            for i in range(totalvacationcard):
#                
#                vacationcardid =   Uservacationcardinfo[i]['id']
#                uservacationcard.append(vacationcardid)
#            userbusinessvacationcardinfo = BusinessCardVacation.objects.values('vacationcard_id').annotate(totalnoofbusinesscard=Count('businesscard_id')).filter(vacationcard_id__in = uservacationcard)
#
#            uservacationtripinfo = VacationTrip.objects.values('vacationcard_id','vacation_name').annotate(stateName=Min('state'),countryName=Min('country'), trip_start_date=Min('trip_start_date'),trip_end_date = Max('trip_end_date')).filter(vacationcard_id__in = uservacationcard)
#            lst = sorted(itertools.chain(userbusinessvacationcardinfo,uservacationtripinfo), key=lambda x:x['vacationcard_id'])
#            list_c = []
#            for k,v in itertools.groupby(lst, key=lambda x:x['vacationcard_id']):
#                d = {}
#                for dct in v:
#                    d.update(dct)
#                list_c.append(d)
#            #print list_c
            queryset = VacationCard.objects.select_related().all().filter(user_id=user_id)
            serializer = VacationCardSerializer(queryset,many=True)
            
            #--------------------------- here we have iterated data to add stard and end date trip -----#
            counter = 0
            for items in serializer.data:
                for key, value in items.items():
                    if key == 'vacation_trips': 
                       counter1 = 1 
                       no_of_stop = len(value)
                       for value1 in sorted(value):
                           if counter1 == 1:
                               serializer.data[counter]['vacation_start_date'] = value1['trip_start_date']
                           if no_of_stop == counter1:
                               serializer.data[counter]['vacation_end_date'] = value1['trip_end_date']
  
                           counter1 = counter1 + 1 
                    
                counter = counter + 1       
                    
            #----------------------------- End ----------------------------------------------------------#               
                           
            if serializer.data:
               return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
            else:
               return CustomeResponse({'msg':"No records found."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1) 
    
    def retrieve(self,request,vacationcard_id=None,call_from_function=None):
        queryset = self.queryset
        vacationtrip_duplicate_data = VacationTrip.objects.filter(vacationcard_id=vacationcard_id)
        serializer = VacationTripSerializer(vacationtrip_duplicate_data,many=True)
        data = {}
        data = serializer.data
                    
        if call_from_function:
            return data
        else:
            return CustomeResponse(data,status=status.HTTP_200_OK)
    
                
    def create(self,request):
        
        try:
            user_id = request.user
        except:
            user_id = None
    
        
        VacationCardserializer = VacationCardSerializer(data=request.DATA,context={'request':request})
        VacationTripserializer = VacationTripSerializer(data=request.DATA,context={'request':request})
      
        try:
            stops = request.DATA['vacation']
            #stops = json.loads(request.DATA['vacation'])
            #stops =  stops["data"]
        except:
            return CustomeResponse({'status':'fail','msg':'Please provide correct Json Format of vacation'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
       # print stops    
        if VacationCardserializer.is_valid():
            vacationid = VacationCardserializer.save(user_id=request.user,vacation_name=request.DATA['vacation_name'])
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
                        tempContainer.append(tempdata['x'])
                    
                     
                        #tempContainer =  tempContainer[0]['x   
                    serializer = VacationTripSerializer(data=tempContainer,many=True)
                    if serializer.is_valid():
                        serializer.save(user_id=request.user)
                        return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
                    else:
                     return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)
        else:
         return CustomeResponse(VacationCardserializer.errors,status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
    
    
    @list_route(methods=['post'],)   
    def duplicate(self,request):
        
            try:           
              user_id = request.user.id
            except:
              user_id = None 
              
            try:
                vacation_id  = request.data['vacation_id']
            except:
                vacation_id =   None
        
            
            if vacation_id:
                #----------------check vacation card belong to user----------#
                from functions import CreateDuplicateVacationCard
                vcard_new  = CreateDuplicateVacationCard(vacation_id,user_id)
                if vcard_new:
                    data =  self.retrieve(request,vacationcard_id=vcard_new,call_from_function=1)
                else:
                   return CustomeResponse({"msg":"some problem occured on server side."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                return CustomeResponse(data,status=status.HTTP_201_CREATED)
            else:
               return CustomeResponse({"msg":"Please provide vcard_id and user_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        

    
    @list_route(methods=['post'],)              
    def delete(self,request):
        
            try:           
              user_id = request.user.id
            except:
              user_id = None 
            
            try:
              vcard_ids = request.data["vcard_ids"]
            except:
              vcard_ids = None
            
            if vcard_ids:
                try:
                    #vcard_ids = json.loads(request.data['vcard_ids'])
                    #vcard_ids = vcard_ids['data']
                    vacation_card = VacationCard.objects.filter(id__in=vcard_ids,user_id =user_id)
                    vacationtrip_info = VacationTrip.objects.filter(vacationcard_id__in=vcard_ids,user_id = user_id)
                    businesscardvacation_info = BusinessCardVacation.objects.filter(vacationcard_id__in=vcard_ids,user_id=user_id)
                    if vacation_card:
                        vacation_card.delete()   
                        vacationtrip_info.delete()
                        if businesscardvacation_info:
                            businesscardvacation_info.delete()
                        return CustomeResponse({'msg':'Vacation card deleted successfully'},status=status.HTTP_201_CREATED)
                    else:
                        return CustomeResponse({'msg':'Vacation card id not found'},status=status.HTTP_201_CREATED)
                except:
                    return CustomeResponse({"msg":"some problem occured on server side during delete vacation cards"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)             
                            

             #------------------------------- End ---------------------------------------------------#
             
             


     
    def destroy(self,request,pk=None):
        #-------For delete first have to call viewvaction API than it will send trip id to delete trip--#
        #------------Delete a single stop in Vacation-----#
        vacation_stop = VacationTrip.objects.filter(id=pk)
        #print vacation_stop
        
        if vacation_stop:
            vacationcard_id = vacation_stop[0].vacationcard_id
            vacation_id  = vacationcard_id.id
            vacation_data = VacationTrip.objects.filter(vacationcard_id=vacation_id)
            vacationcard_data = VacationCard.objects.filter(id=vacation_id)
            businesscard_vacation = BusinessCardVacation.objects.filter(vacationcard_id=vacation_id)
            totalvacationdata =  vacation_data.count()

            if totalvacationdata != 1:
                vacation_stop.delete()
                return CustomeResponse({'msg':'Trip has been deleted'},status=status.HTTP_200_OK)
        
        #------count no of trips of vacation trip if single tripthan  delete trip and vacation card and businesscard vacation---#
        
            if totalvacationdata == 1 :
                vacation_stop.delete()
                vacationcard_data.delete()
                if businesscard_vacation:
                    businesscard_vacation.delete()
            return CustomeResponse({'msg':'Trip and vacation card  has been deleted as you have only one stop in yor vacation'},status=status.HTTP_200_OK)
            
                    
        else:
            print "No trip"
            return CustomeResponse({'msg':'Trip_id not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        

class BusinessCardVacationViewSet(viewsets.ModelViewSet):
    
    queryset = BusinessCardVacation.objects.select_related().all()
    serializer_class    =   BusinessCardVacationSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
    
    def list(self,request):
        #-------------view vacationinfo ------------#
        vacation_id = self.request.QUERY_PARAMS.get('vacationcard_id',None)
        uservacationvacationinfo = dict()
        vacationcard_name = VacationCard.objects.filter(id=vacation_id).values()
        uservacationvacationinfo['vacation_name']= vacationcard_name[0]['vacation_name']
        
        uservacationvacationinfo['trips'] = VacationTrip.objects.filter(vacationcard_id=vacation_id).values().order_by('-id').reverse()
        Uservacationbusinesscardinfo = BusinessCardVacation.objects.filter(vacationcard_id=vacation_id).values()
        
        businesscard_id = []
        for data in Uservacationbusinesscardinfo :
            #print data['businesscard_id_id'] 
            bcard_id = data['businesscard_id_id'] 
            businesscard_id.append(bcard_id)
        
        businesscardinfo = dict()
        businesscardinfo['businessacard'] = BusinessCard.objects.filter(id__in=businesscard_id).values()
        
        uservacationinfo = dict(uservacationvacationinfo, **businesscardinfo)
        
        return CustomeResponse(uservacationinfo,status=status.HTTP_201_CREATED)
    
    def create(self,request):
        
        user_id =  request.user.id
        
        #-----------------------------Apply Multiple Business Card to Multiple Vacation Card------------------#
        
        serializer =    BusinessCardVacationSerializer(data=request.data,context ={'request':request})
        mutable = request.POST._mutable
        request.POST._mutable = True 
        
        try:
            bcard_id =  request.data['businesscard_id']
           # bcard_id = json.loads(request.DATA['businesscard_id'])
            vcard_id =request.DATA['vacationcard_id']
            #vcard_id =  vcard_id['data']
            #bcard_id =  bcard_id['data']
            
            request.DATA['businesscard_id'] = bcard_id[0]  
            request.DATA['vacationcard_id'] = vcard_id[0] 
            request.DATA['user_id']         = user_id
        except:
            return CustomeResponse({'status':'fail','msg':'Please provide businesscard_id'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)


        
        if serializer.is_valid(): 
            #vacationcard_id =  request.data['vacationcard_id'] 
           # user_id =  request.user.id
            tempContainer = []
            count = 0
          
            for data in vcard_id:
                countbcard = 0
                for datavcard in bcard_id:
                    tempdata= {"vacationcard_id":vcard_id[count],"businesscard_id":bcard_id[countbcard],"user_id":user_id}
                    tempContainer.append(tempdata)
                    countbcard = countbcard+1
                count = count +1
        
            businessvacationcardserializer = BusinessCardVacationSerializer(data=tempContainer,many=True)
            if businessvacationcardserializer.is_valid():
                businessvacationcardserializer.save()
                return CustomeResponse(businessvacationcardserializer.data,status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(businessvacationcardserializer.errors,status=status.HTTP_201_CREATED,validate_errors=1)
        else:
                return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED,validate_errors=1)
            
            
    @list_route(methods=['post'],)              
    def delete(self,request):
        #-----------------------------UnApply(Delete) multiple Businesscard to Vacation card ----------#
        
        user_id  = request.user.id
        
        vcard_id = request.DATA['vacationcard_id']
        bcard_id = request.DATA['businesscard_id']
        #bcard_id = bcard_id['data']

        businesscardinfo = BusinessCardVacation.objects.filter(vacationcard_id = vcard_id,businesscard_id__in=bcard_id,user_id=user_id)
        if businesscardinfo:
            businesscardinfo.delete()
            return CustomeResponse({'msg': 'Business card has sucessfully unapply to vacation card'},status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse({'msg':'Id not found Bad request'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
        
class VacationCardMerge(APIView):
    

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
    
    def post(self, request):
        """ 
            merge vaction cards to one vacation card and delete all of thems once done.
            accept from and list of arrays vacation card ids
        """
        try:
            serializer = VacationCardMergeSerializer(data=request.data)
            if serializer.is_valid():
                sourceVacationCardIds = request.data.get('source')
                destVacationCardId = request.data.get('dest')
                vacationCardIds = sourceVacationCardIds[:]
                vacationCardIds.append(destVacationCardId)
               
                vacationCardCount = VacationCard.objects.filter(user_id=request.user, id__in=vacationCardIds).count()
                
                # ids must be belongs to session user and not dest id not in source
                if vacationCardCount != len(vacationCardIds):
                    return CustomeResponse({'msg': 'one or all of the vacation ids not exists'}, status=status.HTTP_400_BAD_REQUEST)
                
                VacationTrip.objects.filter(user_id=request.user, vacationcard_id__in=sourceVacationCardIds).update(vacationcard_id=destVacationCardId)
                VacationTrip.objects.filter(user_id=request.user, vacationcard_id__in=sourceVacationCardIds).update(vacationcard_id=destVacationCardId)

                
                #remove source vacation card once it trips done
                VacationCard.objects.filter(user_id=request.user, id__in=sourceVacationCardIds).delete()
                
                return CustomeResponse({'msg':'success'}, status=status.HTTP_200_OK)
        except:
            return CustomeResponse({'msg':'Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return CustomeResponse({'msg': 'data format error, integer required'}, status=status.HTTP_400_BAD_REQUEST)
