#----------------------------------------------#
# Developer Name: Sajid
# Creation Date: 2015/08/04
# Notes: View File
#----------------------------------------------#
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import User,Profile,SocialLogin
from serializer import UserSerializer,ProfileSerializer,SocialLoginSerializer
from ohmgear.authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ohmgear.functions import custome_response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
# Create your views here.
# User View Prototype which will same format for other view
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    authentication_classes = (ExpiringTokenAuthentication,)
#    permission_classes = (IsAuthenticated,)

    def set_password(self,request,user_id):
      try:
        user = get_user_model().objects.get(id=user_id) 
        user.set_password(request.DATA['password'])
        user.save()
        return True
      except:
        return False  
        
                            
    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True,context={'request': request})
        return Response(custome_response(serializer.data,error=0))

    def retrieve(self, request):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(user,context={'request': request})
        return Response(custome_response(serializer.data,error=0))

    def create(self, request):
         
         serializer =  UserSerializer(data=request.DATA,context={'request': request})
         if serializer.is_valid():
            user_id=serializer.save() 
            #---------------- Set the password -----------#
            if request.DATA['password'] and request.DATA['password'] is not None:
               self.set_password(request,user_id.id)
            #---------------- End ------------------------#
            
            return Response(custome_response(serializer.data,error=0))
         else:
            return Response(custome_response(serializer.errors,error=1))

    def update(self, request, pk=None):
         try:
           messages = User.objects.get(id=pk)
         except:
           return Response(status=status.HTTP_404_NOT_FOUND)
       
         serializer =  UserSerializer(messages,data=request.DATA,partial=True,context={'request': request})
         if serializer.is_valid():
            serializer.save()
            #---------------- Set the password -----------#
            if request.DATA['password'] and request.DATA['password'] is not None:
               self.set_password(request,pk)
            #---------------- End ------------------------#            
            return Response(custome_response(serializer.data,error=0))
         else:
            return Response(custome_response(serializer.errors,error=1))

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass    


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    
class SocialLoginViewSet(viewsets.ModelViewSet):
    queryset = SocialLogin.objects.all()
    serializer_class = SocialLoginSerializer
