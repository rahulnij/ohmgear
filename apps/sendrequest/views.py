#------------ Third Party Imports ----------#
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status
import boto3
#------------ Third Party Imports ----------#
#------------------ Local app imports ------#
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
from models import Notification 
from apps.businesscards.models import BusinessCard
from apps.awsserver.models import AwsDeviceToken
from apps.users.models import Profile
import json
#---------------------------End-------------#
# Create your views here.

class SendNotification(viewsets.ModelViewSet):

    queryset  = Notification.objects.all()
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
    def invite_to_businesscard(self, request):
        user_id  =request.user   
        try:
          to_business_card_id  =request.DATA['to_business_card_id'] 
          from_business_card_id  =request.DATA['from_business_card_id']
          device_token  =request.DATA['device_token']
          get_profile = Profile.objects.filter(user_id=user_id).values("first_name","last_name").latest("id")
          user_name = str(get_profile["first_name"])+" "+str(get_profile["last_name"])
        except:
          return CustomeResponse({'msg':"Please provide to_business_card_id,from_business_card_id and device_token"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)     
        
       
        #check from_business_card_id belongs to user_id 
        try:
         business_card_from = BusinessCard.objects.filter(user_id=user_id.id,id = from_business_card_id).latest("id")
         business_card_to  = BusinessCard.objects.filter(id = to_business_card_id).exclude(user_id=user_id.id).latest("id")
        except:
         return CustomeResponse({'msg':"Provided business cards are not correct"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)     
        
        #--- Get the aws arn from token table ------------------#
        try:
          aws_token_data = AwsDeviceToken.objects.filter(user_id=business_card_to.user_id.id,device_token=device_token).latest("id")
        except:
          return CustomeResponse({'msg':"to_business_card_id device token does not exist."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
        #aws_plateform_endpoint_arn = '%s'%aws_token_data.aws_plateform_endpoint_arn
        #---------- End ----------------------------------------#
        client = boto3.client('sns')
        #------------ Make json to send data ---------------------#
        message = {
                   'default':'request sent from '+user_name+' to accept businesscard11.', 
                   'APNS_SANDBOX':{'aps':{'alert':'Hi How are you'},'data':{
                    'business_card_from':business_card_from.id,
                    'business_card_to':business_card_to.id,
                    }},
                   
                  }
        message = json.dumps(message,ensure_ascii=False)          
        print message
        #------------------------ End ----------------------------#
        response = client.publish(
            TargetArn= aws_token_data.aws_plateform_endpoint_arn,
            Message=message,
            Subject='Hello vijay',
            MessageStructure='json',
            MessageAttributes={               
            }
        )                           
        return CustomeResponse(response,status=status.HTTP_200_OK)
    
    
    