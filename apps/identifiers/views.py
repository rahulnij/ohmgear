from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import Identifier
from serializer import IdentifierSerializer
from ohmgear.functions import CustomeResponse
from rest_framework.decorators import api_view
import rest_framework.status as status
#import random
from functions import CreateSystemIdentifier


# Create your views here.
class IdentifierViewSet(viewsets.ModelViewSet):
    queryset = Identifier.objects.select_related().all()
    serializer_class = IdentifierSerializer
    
    #--------------Method: GET-----------------------------#       
    def list(self,request,**kwargs):
        if request.method == 'GET':
            user =  self.request.QUERY_PARAMS.get('user', None)
            userdata = Identifier.objects.filter(user=user).values()
            return CustomeResponse(userdata,status=status.HTTP_201_CREATED)
    
                
            
    #--------------Method: GET retrieve single record-----------------------------#
    def retrieve(self, request,pk=None):
        queryset = self.queryset
        identifier = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(identifier,context={'request': request})
        
        return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
    
    #--------------Method: POST create new Identifier -----------------------------#
    def create(self, request,fromsocial=None):
         
         serializer =  IdentifierSerializer(data=request.DATA,context={'request': request})
         
         #print data
         #request.DATA['identifier'] = (''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for i in range(6)))
         #------ object value which can be change are mutable object value which cannot be change are immutable  -----------#
         mutable = request.POST._mutable
         request.POST._mutable = True
        
         if request.POST.get('identifier_type') == '1':
            request.POST['identifier'] =   CreateSystemIdentifier()
         else: 
           pass
         request.POST._mutable = mutable
         serializer =  IdentifierSerializer(data=request.DATA,context={'request': request,'msg':'not exist'})
         
         if serializer.is_valid():
             
            #------------ enable/desable signal -----------------#
            if fromsocial:
                self._disable_signals = True
            #------------ End -----------------------------------#
            
            identifier_id=serializer.save()  
            if not fromsocial:
             return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
            else:
             return serializer.data   
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    

