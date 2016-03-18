#------------ Third Party Imports ----------#
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status
from django.conf import settings
import boto3
#------------ Third Party Imports ----------#
#------------------ Local app imports ------#
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
from models import AwsDeviceToken 
#---------------------------End-------------#
# Create your views here.

class AWSActivity(viewsets.ModelViewSet):

    queryset  = AwsDeviceToken.objects.all()
    serializer_class = None
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def list(self,request):
        return CustomeResponse({'msg':"GET METHOD NOT ALLOWD"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  
    def create(self,request,call_from_function=None,offline_data=None):
        return CustomeResponse({'msg':"POST METHOD NOT ALLOWD"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   
    def destroy(self, request, pk=None):
        return CustomeResponse({'msg':"DELETE METHOD NOT ALLOWD"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)  
    
    
    @list_route(methods=['post'],)
    def register_to_aws(self, request):
        user_id  =request.user
        try:
           device_token  =request.DATA['device_token']
           device_type  =request.DATA['device_type']
        except:
           return CustomeResponse({'msg':"Please provide device_token,device_type"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)       
        
        if device_type == 'apns':
           platform_application_arn = settings.AWS_PLATEFORM_APPLICATION_ARN["APNS"]
        elif device_type == 'gcm':
           platform_application_arn = settings.AWS_PLATEFORM_APPLICATION_ARN["GCM"] 
        else:
           return CustomeResponse({'msg':"device_type must be apns or gcm"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)          
        return CustomeResponse({'msg':platform_application_arn},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)             
        if device_token and user_id and device_type:            
           client = boto3.client('sns')
           #--- TODO Need to check device token already exist or not ---#
           
           #--------- End-----------------------------------------------#           
           try:  
                response = client.create_platform_endpoint(
                             PlatformApplicationArn=platform_application_arn,
                             Token=device_token,
                             CustomUserData='',
                             Attributes={
                                 #'string': 'string'
                             }
                            )            
                if "EndpointArn" in response:
                    AwsDeviceToken.objects.update_or_create(device_token=device_token,aws_plateform_endpoint_arn=response["EndpointArn"],user_id=user_id,device_type=device_type)                    
                    
           except:
                return CustomeResponse({'msg':"this token already attached to provided plateform application"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   
           
           return CustomeResponse(response,status=status.HTTP_200_OK)
        else:
           return CustomeResponse({'msg':"Please provide device_token,device_type and user token"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)   
        


    
        
    
    
    