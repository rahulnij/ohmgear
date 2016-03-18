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
from apps.folders.models import Folder,FolderContact
import json
import ohmgear.settings.aws as aws
#---------------------------End-------------#
# Create your views here.

class SendAcceptRequest(viewsets.ModelViewSet):

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
    
    #-------------------- local class function --------------------------------#
    def insert_notification(self,type,sender_id,receiver_id,message):
       try: 
        notification = Notification()
        notification.type = type
        notification.sender_id = sender_id
        notification.receiver_id = receiver_id
        notification.message = message
        notification.save()
        return True
       except:
        return False   
    #-------------------------- End -------------------------------------------#
    
    @list_route(methods=['post'],)
    def invite_to_businesscard(self, request):
        user_id  =request.user   
        try:
          receiver_business_card_id  =request.DATA['receiver_business_card_id'] 
          sender_business_card_id  =request.DATA['sender_business_card_id']
          device_token  =request.DATA['device_token']
          get_profile = Profile.objects.filter(user_id=user_id).values("first_name","last_name").latest("id")
          user_name = str(get_profile["first_name"])+" "+str(get_profile["last_name"])
        except:
          return CustomeResponse({'msg':"Please provide receiver_business_card_id,sender_business_card_id and device_token"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)     
        
       
        #check from_business_card_id belongs to user_id 
        try:
         sender_business_card = BusinessCard.objects.filter(user_id=user_id.id,id = sender_business_card_id).latest("id")
         receiver_business_card  = BusinessCard.objects.filter(id = receiver_business_card_id).exclude(user_id=user_id.id).latest("id")
        except:
         return CustomeResponse({'msg':"Provided business cards are not correct"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)     
        
        #--- Get the aws arn from token table ------------------#
        try:
          aws_token_data = AwsDeviceToken.objects.filter(user_id=receiver_business_card.user_id.id).latest("id")
        except:
          return CustomeResponse({'msg':"receiver device token does not exist."},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
        #aws_plateform_endpoint_arn = '%s'%aws_token_data.aws_plateform_endpoint_arn
        #---------- End ----------------------------------------#
        client = boto3.client('sns',**aws.AWS_CREDENTIAL)
        #------------ Make json to send data ---------------------#
        message = {
                   'default':'request sent from '+user_name+' to accept businesscard.', 
                   'APNS_SANDBOX':{'aps':{'alert':'Hi How are you'},'data':{
                    'receiver_business_card_id':receiver_business_card_id,
                    'sender_business_card_id':sender_business_card_id,
                    }},
                   
                  }
        message = json.dumps(message,ensure_ascii=False)  
        #------------------------ End ----------------------------#
        #--- TODO If user install app more then one device then send the notification more then one device ---#
        #--- End ---#
        response = client.publish(
            TargetArn= aws_token_data.aws_plateform_endpoint_arn,
            Message=message,
            MessageStructure='json',
            MessageAttributes={               
            }
        )
        #--- Insert into Notification Table ---#
        type = 'b2b'
        sender_id = sender_business_card_id
        receiver_id = receiver_business_card_id
        message = 'request sent from '+user_name+' to accept businesscard.'
        self.insert_notification(type,sender_id,receiver_id,message)
        #--------- End-----------------------------------------------#         
        return CustomeResponse(response,status=status.HTTP_200_OK)
    
    

    
    #----------------------------------------------------------------------------------------------------#
    #----------------------------------- Receive Request ------------------------------------------------#
    
    @list_route(methods=['post'],)
    def accept_businesscard(self, request):
        user_id  =request.user
        try:
          receiver_business_card_id  =request.DATA['receiver_business_card_id'] 
          sender_business_card_id  =request.DATA['sender_business_card_id']
        except:
          return CustomeResponse({'msg':"Please provide sender_business_card_id,receiver_business_card_id"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)       
          
        try:
         sender_business_card = BusinessCard.objects.select_related("contact_detail").get(user_id=user_id.id,id = sender_business_card_id)
         receiver_business_card  = BusinessCard.objects.select_related("contact_detail").exclude(user_id=user_id.id).get(id = receiver_business_card_id)
        except:
         return CustomeResponse({'msg':"Provided business cards are not correct"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)           
        
        
        sender_contact_id =  sender_business_card.contact_detail.id
        receiver_contact_id =  receiver_business_card.contact_detail.id
        
        try:
          sender_folder = Folder.objects.get(businesscard_id=sender_business_card_id)
          sender_folder_id = sender_folder.id
        except:
          return CustomeResponse({'msg':"sender businesscard dont have folder"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)             
        
        try:
          receiver_folder = Folder.objects.get(businesscard_id=receiver_business_card_id)
          receiver_folder_id = receiver_folder.id
        except:
          return CustomeResponse({'msg':"receiver businesscard dont have folder"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)         
    
        #--------------------- Now we are inserting data in folder contact table for making connection -----#
        try:
          folder_sender= FolderContact.objects.get(folder_id = sender_folder,contact_id = receiver_business_card.contact_detail)
        except:
            folder_sender= FolderContact()
            folder_sender.user_id = user_id
            folder_sender.folder_id = sender_folder
            folder_sender.contact_id = receiver_business_card.contact_detail
            folder_sender.link_status = 2
            folder_sender.save()
        try:
           folder_receiver= FolderContact.objects.get(user_id = user_id,folder_id = receiver_folder)
        except:
            folder_receiver= FolderContact()
            folder_receiver.user_id = receiver_business_card.user_id
            folder_receiver.folder_id = receiver_folder
            folder_receiver.contact_id = sender_business_card.contact_detail
            folder_receiver.link_status = 2
            folder_receiver.save()        
        #--------------------------------- End -------------------------------------------------------------#
        
        return CustomeResponse({"msg":"success"},status=status.HTTP_200_OK)