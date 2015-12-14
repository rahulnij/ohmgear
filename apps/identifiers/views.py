from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import Identifier
from apps.businesscards.models import BusinessCardIdentifier
from serializer import IdentifierSerializer
from apps.businesscards.serializer import BusinessCardIdentifierSerializer
from ohmgear.functions import CustomeResponse
from rest_framework.decorators import api_view
import rest_framework.status as status
from datetime import date
import datetime
import random
from functions import CreateSystemIdentifier
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class IdentifierViewSet(viewsets.ModelViewSet):
    queryset = Identifier.objects.select_related().all()
    serializer_class = IdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 
    #--------------Method: GET-----------------------------#       
    def list(self,request,**kwargs):
        if request.method == 'GET':
            
            identifier =  self.request.QUERY_PARAMS.get('identifier', None)
            
            # -----------check whether idnetifier is exist or not if not give suggested identifier--------#
            identifierdata = Identifier.objects.filter(identifier=identifier).values()
            
            # -----------Get all identifiers of the user--------#
            user =  self.request.QUERY_PARAMS.get('user', None)
            #userdata = Identifier.objects.filter(user=user).values().order_by('-id')
            
            userdata = Identifier.objects.select_related('businesscard_identifiers').filter(user=user).order_by('-id')
            
           # queryset = VacationCard.objects.select_related().all().filter(user_id=user_id)
            serializer = IdentifierSerializer(userdata,many=True)
            
            
            if userdata:
                return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
            else:
                if identifier is None:
                    return CustomeResponse({'msg':'user id is not exist'},status=status.HTTP_201_CREATED)
                if not identifierdata and identifier is not None:
                    return CustomeResponse({'msg':'Identifier available'},status=status.HTTP_201_CREATED)
                
                else:
                    list = []
                    for i in range(5):
                        identifiersuggestion=''.join(random.choice('0123456789') for i in range(2))
                        newidentifier = identifier + identifiersuggestion
                        matchidentifier = Identifier.objects.filter(identifier=newidentifier).values()
                        if not matchidentifier:
                           list.append(newidentifier)
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
         
         #print businesscard_id
         #------ object value which can be change are mutable object value which cannot be change are immutable  -----------#
         mutable = request.POST._mutable
         request.POST._mutable = True
         request.DATA['identifierlastdate'] = str((datetime.date.today() + datetime.timedelta(3*365/12)).isoformat())
            
        
         if request.POST.get('identifiertype') == '1':
            request.POST['identifier'] =   CreateSystemIdentifier()
         else: 
           pass
         #request.POST._mutable = mutable
         serializer =  IdentifierSerializer(data=request.DATA,context={'request': request,'msg':'not exist'})
         
         if serializer.is_valid():
            identifier_id = serializer.save()      
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)        
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    
    

