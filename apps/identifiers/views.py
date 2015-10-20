from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import Identifier
from serializer import IdentifierSerializer
from ohmgear.functions import CustomeResponse
from rest_framework.decorators import api_view
import rest_framework.status as status
from datetime import date
import datetime
import random
from functions import CreateSystemIdentifier
from cron import  my_scheduled_job

# Create your views here.
class IdentifierViewSet(viewsets.ModelViewSet):
    queryset = Identifier.objects.select_related().all()
    serializer_class = IdentifierSerializer
    
    #--------------Method: GET-----------------------------#       
    def list(self,request,**kwargs):
        if request.method == 'GET':
            
            identifier =  self.request.QUERY_PARAMS.get('identifier', None)
            identifierdata = Identifier.objects.filter(identifier=identifier).values()
            user =  self.request.QUERY_PARAMS.get('user', None)
            userdata = Identifier.objects.filter(user=user).values()
            if userdata:
                print userdata
                return CustomeResponse(userdata,status=status.HTTP_201_CREATED)
            else:
                if not identifierdata:
                    return CustomeResponse({'msg':'Identifier available'},status=status.HTTP_201_CREATED)
                
                else:
                    print "already exist"
                    print identifier
                    list = []
                    for i in range(5):
                        
                        identifiersuggestion=''.join(random.choice('0123456789') for i in range(2))
                        print "identifiersuggestion"
                        print identifiersuggestion
                        #data  =insert_list.append(Identifier(identifier=identifier))
                        newidentifier = identifier + identifiersuggestion
                        print "newidentifier"
                        print newidentifier
                        matchidentifier = Identifier.objects.filter(identifier=newidentifier).values()
                        print "matchidentifier"
                        print matchidentifier
                        if not matchidentifier:
                           print newidentifier
                           list.append(newidentifier)
                           #list = identifier
                    
                    return CustomeResponse({'msg':list},status=status.HTTP_200_OK,validate_errors=1)
    
                
            
    #--------------Method: GET retrieve single record-----------------------------#
    def retrieve(self, request,pk=None):
        queryset = self.queryset
        identifier = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(identifier,context={'request': request})
        
        return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
    
    #--------------Method: POST create new Identifier -----------------------------#
    def create(self, request):
         
         serializer =  IdentifierSerializer(data=request.DATA,context={'request': request})
         
         #print data
         #request.DATA['identifier'] = (''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(6)))
         #------ object value which can be change are mutable object value which cannot be change are immutable  -----------#
         mutable = request.POST._mutable
         request.POST._mutable = True
         request.DATA['idetifierlastdate'] = str((datetime.date.today() + datetime.timedelta(3*365/12)).isoformat())
        #----------------------------- 
        
         #my_scheduled_job()
         
         if request.POST.get('identifier_type') == '1':
            request.POST['identifier'] =   CreateSystemIdentifier()
         else: 
           pass
         #request.POST._mutable = mutable
         serializer =  IdentifierSerializer(data=request.DATA,context={'request': request,'msg':'not exist'})
         
         if serializer.is_valid():
            serializer.save()  
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
            
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    
    

