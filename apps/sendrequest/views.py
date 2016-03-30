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
from serializer import NotificationSerializer
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
import hashlib, datetime, random
from apps.email.views import BaseSendMail
#---------------------------End-------------#
# Create your views here.

class SendNotification(viewsets.ModelViewSet):
    
    queryset  = Notification.objects.all()
    serializer_class = NotificationSerializer
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
        
        client = boto3.client('sns')
#        response = client.list_topics()
        response = client.publish(
            #TopicArn='',
            TargetArn='arn:aws:sns:ap-southeast-1:625053715246:endpoint/APNS_SANDBOX/KINBOW/1cd49ef5-734b-3d52-8ac3-65aaa3acc341',
            Message='Hello vijay',
            Subject='Hello vijay',
            MessageStructure='string',
            MessageAttributes={               
            }
        )                           
        return CustomeResponse(response,status=status.HTTP_200_OK)
    
    @list_route(methods=['post'],)
    def send_white_invitation(self, request):

        authentication_classes = (ExpiringTokenAuthentication,)
        permission_classes = (IsAuthenticated,)
        try:
            user_id = request.user
        except:
            user_id = None

        data = {}
        data['sender_id'] = request.user.id
        data['type'] = request.user.user_type_id
        data['receiver_id'] = request.DATA.get('receiver_id')
        data['message'] = request.DATA.get('message')

        fname = data['message']['fname']
        lname = data['message']['lname']
        email = data['message']['email']
        contactId = data['receiver_id']
        sid = str(data['sender_id'])
        
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt+email).hexdigest()[:10]
         
        data['object_pk_url'] = str(settings.DOMAIN_NAME)+ "/api/greyrequest/invite_registration"+ "/?email="+email+"&fname="+fname+"&lname="+lname+"&cid="+contactId+"&sid="+sid
    
        serializer = NotificationSerializer(data=data,context ={'request':request,'msg':'not exist'})
        
        if serializer.is_valid():
                serializer.save()
                #BaseSendMail.delay(data,type='grey_invitation',key = activation_key)
                return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse({'msg':serializer.errors},validate_errors=1)
        
        
    @list_route(methods=['post'],)
    def rest_invitation(self, request):
        
        try:
            user_id = request.user.id
        except:
            user_id = None
        print user_id
        queryset_folder = Notification.objects.filter(receiver_id=user_id,read_status=0).values()
        if  queryset_folder:
            return CustomeResponse({'msg':queryset_folder},status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse({'msg':"data not found"},validate_errors=1)
    
    
        
     
    
class GreyInvitationViewSet(viewsets.ModelViewSet):
    
    queryset  = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    @list_route(methods=['get'],)
    def invite_registration(self, request):
        
        email = request.GET.get('email')
        fname = request.GET.get('fname')
        lname = request.GET.get('lname')
        cid = request.GET.get('cid')
        sid = request.GET.get('sid')
             
        return render_to_response('templates/index.html', {'email': email,'fname':fname,'lname':lname,'cid':cid,'sid':sid})
    

     

    