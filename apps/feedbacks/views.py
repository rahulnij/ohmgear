from django.shortcuts import render
from rest_framework import routers,serializers,viewsets
from models import Feedbacks
from serializer import FeedbacksSerializer
from ohmgear.functions import CustomeResponse
import rest_framework.status as status

from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbacksSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes     =  (IsAuthenticated,)
    
    def create(self,request):
        userid =  request.user.id
        tempData = request.data.copy()
        tempData['user_id'] = userid
        serializer = FeedbacksSerializer(data=tempData,context={'request':request})
        if serializer.is_valid():        
            serializer.save()
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
    
    