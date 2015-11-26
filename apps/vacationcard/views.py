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
from rest_framework.decorators import detail_route


class VacationCardViewSet(viewsets.ModelViewSet):
    queryset = VacationTrip.objects.select_related().all()
    #serializer_class = VacationTripSerializer
    serializer_class = VacationCardSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
    #--------------Method: GET-----------------------------#       
    def list(self,request):
        
        if request.method == 'GET':
           #-----------get all vacations of the user and no of business card attached to it------# 
           # user = user_profile.user
            user_id =  request.user.id
            #print user_id
            #user_id =   self.request.QUERY_PARAMS.get('user_id',None)
            Uservacationcardinfo = VacationCard.objects.filter(user_id=user_id).values()
            totalvacationcard =  Uservacationcardinfo.count()
            uservacationcard = []
            for i in range(totalvacationcard):
                
                vacationcardid =   Uservacationcardinfo[i]['id']
                uservacationcard.append(vacationcardid)
            userbusinessvacationcardinfo = BusinessCardVacation.objects.values('vacationcard_id').annotate(totalnoofbusinesscard=Count('businesscard_id')).filter(vacationcard_id__in = uservacationcard)

            uservacationtripinfo = VacationTrip.objects.values('vacationcard_id','country','state','contact_no','notes','user_id').annotate(trip_start_date=Min('trip_start_date'),trip_end_date = Max('trip_end_date')).filter(vacationcard_id__in = uservacationcard)
                
                
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
        
        try:
           op = request.data["op"]
        except:             
           op = None
           
         #---------------------------- Delete Vacation Card -------------------------------------#         
        if op == 'delete':
            try:
              vcard_ids = request.data["vcard_ids"]
            except:
              vcard_ids = None
            if vcard_ids:
                try:
                    vcard_ids = vcard_ids.split(",")
                    vcard_ids = filter(None, vcard_ids)
                    vacation_card = VacationCard.objects.filter(id__in=vcard_ids)
                    vacationtrip_info = VacationTrip.objects.filter(vacationcard_id__in=vcard_ids)
                    businesscardvacation_info = BusinessCardVacation.objects.filter(vacationcard_id__in=vcard_ids)
                    if vacation_card:
                        vacation_card.delete()   
                        vacationtrip_info.delete()
                        businesscardvacation_info.delete()
                        return CustomeResponse({'msg':'Vacation card deleted successfully'},status=status.HTTP_201_CREATED)
                    else:
                        return CustomeResponse({'msg':'Vacation card id not found'},status=status.HTTP_201_CREATED)
                except:
                    return CustomeResponse({"msg":"some problem occured on server side during delete business cards"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)             
#                        
         
         #------------------------------- End ---------------------------------------------------#
        
        
        
        VacationCardserializer = VacationCardSerializer(data=request.DATA,context={'request':request})
        VacationTripserializer = VacationTripSerializer(data=request.DATA,context={'request':request})
      
        try:
            vacation = request.DATA['vacation']
            stops = json.loads(request.DATA['vacation'])
            stops =  stops["data"]
        except:
            return CustomeResponse({'status':'fail','msg':'Please provide correct Json Format of vacation'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
       # print stops    
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
                        tempContainer.append(tempdata['x'])
                    
                     
                        #tempContainer =  tempContainer[0]['x   
                    serializer = VacationTripSerializer(data=tempContainer,many=True)
                    if serializer.is_valid():
                        serializer.save()
                        return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
                    else:
                     return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)
        else:
         return CustomeResponse(VacationCardserializer.errors,status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)
     
     
    def destroy(self,request,pk=None):
        #-------For delete first have to call viewvaction API than it will send trip id to delete trip--#
        #------------Delete a single stop in Vacation-----#
        vacation_stop = VacationTrip.objects.filter(id=pk)
        
        if vacation_stop:
            vacation_stop.delete()
            return CustomeResponse({'msg':'Trip has been deleted'},status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg':'Trip_id not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

    

class VacationCardMerge(APIView):

    def post(self, request):
        """ 
            merge vaction cards to one vacation card and delete all of thems once done.
            accept from and list of arrays vacation card ids
        """
        print request.data



class BusinessCardVacationViewSet(viewsets.ModelViewSet):
    
    queryset = BusinessCardVacation.objects.select_related().all()
    serializer_class    =   BusinessCardVacationSerializer
    
    def list(self,request):
        #-------------view vacationinfo ------------#
        vacation_id = self.request.QUERY_PARAMS.get('vacationcard_id',None)
        uservacationvacationinfo = dict()
        uservacationvacationinfo['trips'] = VacationTrip.objects.filter(vacationcard_id=vacation_id).values()
        Uservacationbusinesscardinfo = BusinessCardVacation.objects.filter(vacationcard_id=vacation_id).values()
        #print Uservacationbusinesscardinfo
        
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
        
        #-----------------------------UnApply(Delete) Businesscard to Vacation ----------#
        try:
            op = request.DATA['op']
        except:
            op =None
        
        if op == 'delete':
            vcard_id = request.DATA['vacationcard_id']
            bcard_id = json.loads(request.DATA['businesscard_id'])
            bcard_id = bcard_id['data']
            
            businesscardinfo = BusinessCardVacation.objects.filter(vacationcard_id = vcard_id,businesscard_id__in=bcard_id)
            if businesscardinfo:
                businesscardinfo.delete()
                return CustomeResponse({'msg': 'Business card has sucessfully unapply to vacation card'},status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse({'msg':'Id not found Bad request'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
        
        
        #---------------------------------End-----------------------------------------------#
        
        #-----------------------------Apply Multiple Business Card to Multiple Vacation Card------------------#
        
        serializer =    BusinessCardVacationSerializer(data=request.data,context ={'request':request})
        mutable = request.POST._mutable
        request.POST._mutable = True 
        
        try:
            businesscard_id =  request.data['businesscard_id']
            bcard_id = json.loads(request.DATA['businesscard_id'])
            vcard_id =json.loads(request.DATA['vacationcard_id'])
            vcard_id =  vcard_id['data']
            bcard_id =  bcard_id['data']
            request.DATA['businesscard_id'] = bcard_id[0]  
            request.DATA['vacationcard_id'] = vcard_id[0]  
        except:
            return CustomeResponse({'status':'fail','msg':'Please provide businesscard_id'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)


        
        if serializer.is_valid(): 
            #vacationcard_id =  request.data['vacationcard_id'] 
            user_id =  request.data['user_id'] 
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
            
            
            
            
            
#            for data in bcard_id:
#                #print bcard_id[count]
#                tempdata = {"vacationcard_id":vacationcard_id,"businesscard_id":bcard_id[count],"user_id":user_id}
#                tempContainer.append(tempdata)
#                count = count+1
#            businessvacationcardserializer = BusinessCardVacationSerializer(data=tempContainer,many=True)    
#            if businessvacationcardserializer.is_valid(): 
#                businessvacationcardserializer.save()
#                return CustomeResponse(businessvacationcardserializer.data,status=status.HTTP_201_CREATED)
#            else:
#                return CustomeResponse(businessvacationcardserializer.errors,status=status.HTTP_201_CREATED,validate_errors=1)
#        else:
#                return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED,validate_errors=1)
            
            
            
        #--------------------------------------End----------------------------------------------------------#
            