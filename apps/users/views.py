#----------------------------------------------#
# Developer Name: Sajid
# Creation Date: 2015/08/04
# Notes: View File
#----------------------------------------------#
from rest_framework import viewsets
from models import User,Profile,SocialLogin
from serializer import UserSerializer,ProfileSerializer,SocialLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import custome_response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from models import SocialLogin

# Create your views here.
# User View Prototype which will same format for other view
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #authentication_classes = (ExpiringTokenAuthentication,)
    #permission_classes = (IsAuthenticated,)

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
    
    def create(self, request):    
       
        
               
                serializer =  UserSerializer(data=request.DATA,context={'request': request})
                #print get_user_model().objects.filter(email=request.DATA['email'])
                if get_user_model().objects.filter(email=request.DATA['email']): 
                    return Response(custome_response(serializer.data,error=0))  
                else:
                    if serializer.is_valid():
                        user_id = serializer.save()
                        social_id = request.POST.get('social_id','')
                        sociallogin = SocialLogin(user_id=user_id.id,social_media_login_id = social_id)
                        sociallogin.save()
                        #serializer_class = SocialLoginSerializer(data= user_id)
                        return Response(custome_response(sociallogin.data,error=0))
                        #return Response(custome_response(serializer.errors,error=1))
                    else:
                       return Response(custome_response(serializer.errors,error=1)) 
        #except:
            #return Response(custome_response(serializer.errors,error=1))

            
#----------User Login | Forgot Password | Reset Password -----------------#      
@api_view(['GET','POST'])       
def useractivity_list(request):
    msg = {}
    if request.method == 'GET':
     pass        
    if request.method == 'POST':
        op = request.POST.get('op','')
        # ----------- Login ------------------#
        if op == 'login':
            
             pass
             
             return Response(user[0])
        else:
             return Response('Not Found',status=status.HTTP_404_NOT_FOUND)            
