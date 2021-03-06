# --------- Import Python Modules ----------- #

import boto3
import hashlib
import random
import json
# ------------ Third Party Imports ---------- #
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status
from django.conf import settings

# ----------------- Local app imports ------ #
from apps.email.views import BaseSendMail
from apps.sendrequest.serializer import SendRequestSerializer
from models import SendRequest
from apps.businesscards.models import BusinessCard
from apps.users.models import Profile
from apps.users.models import User
from apps.folders.models import Folder, FolderContact
from apps.awsserver.models import AwsDeviceToken
import ohmgear.settings.aws as aws
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
import logging
# ---------------------------End------------- #
logger = logging.getLogger(__name__)


class SendAcceptRequest(viewsets.ModelViewSet):

    queryset = SendRequest.objects.all()
    serializer_class = None
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        return CustomeResponse({'msg': "GET METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def create(self, request, call_from_function=None, offline_data=None):
        return CustomeResponse({'msg': "POST METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def destroy(self, request, pk=None):
        return CustomeResponse({'msg': "DELETE METHOD NOT ALLOWD"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    # -------------------- local class function ----------------------- #
    def insert_notification(self, **karg):
        # Required data
        # sender_user_id
        # sender_business_card_id  => Object of business card
        # receiver_user_id
        # receiver_bcard_or_contact_id
        # message
        # request_type
        try:
            notification = SendRequest()

            notification.request_type = karg['request_type']
            notification.sender_user_id = karg['sender_user_id']
            notification.sender_business_card_id = karg[
                'sender_business_card_id']

            notification.receiver_user_id = karg['receiver_user_id']
            notification.receiver_bcard_or_contact_id = karg[
                'receiver_bcard_or_contact_id']

            notification.message = karg['message']

            try:
                notification.save()
                return True
            except Exception as e:
                logger.critical(
                    "Unhandled exception in {}, {}".format(
                        __name__, e))
                return False

        except Exception as e:
            logger.critical(
                "Unhandled exception in {}, {}".format(
                    __name__, e))
            return False

    def exchange_business_cards(self, **karg):

        # Required data
        # sender_folder
        # sender_business_card object with contact_detail
        # receiver_folder
        # receiver_business_card object with contact_detail
        # sender_user_id # we can also get this from sender_business_card

        try:
            receiver_contact_id = karg['receiver_business_card'].contact_detail
        except:
            # from white contact request directly sending receiver_contact_id
            try:
                receiver_contact_id = karg['receiver_contact_id']
            except KeyError as e:
                logger.error(
                    "KeyError in {}, {}".format(
                        __name__, e))
                return False

        try:
            sender_contact_id = karg['sender_business_card'].contact_detail
        except:
            # from white contact request directly sending receiver_contact_id
            try:
                sender_contact_id = karg['sender_contact_id']
            except KeyError as e:
                logger.error(
                    "KeyError in {}, {}".format(
                        __name__, e))
                return False

        # --- we are checking link already exist as white contact have other user contact already
        try:
            folder_sender = FolderContact.objects.get(
                folder_id=karg['sender_folder'], contact_id=receiver_contact_id)
            folder_sender.link_status = 2
            folder_sender.is_linked = 1
            folder_sender.save()
        except FolderContact.DoesNotExist as e:

            folder_sender = FolderContact()
            folder_sender.user_id = karg['sender_user_id']
            folder_sender.folder_id = karg['sender_folder']
            folder_sender.contact_id = receiver_contact_id
            folder_sender.link_status = 2
            folder_sender.is_linked = 1
            folder_sender.save()

        try:
            folder_receiver = FolderContact.objects.get(
                folder_id=karg['receiver_folder'], contact_id=sender_contact_id)
            folder_receiver.link_status = 2
            folder_receiver.is_linked = 1
            folder_receiver.save()
        except FolderContact.DoesNotExist as e:

            folder_receiver = FolderContact()
            folder_receiver.user_id = receiver_contact_id.user_id
            folder_receiver.folder_id = karg['receiver_folder']
            folder_receiver.contact_id = sender_contact_id
            folder_receiver.link_status = 2
            folder_receiver.is_linked = 1
            folder_receiver.save()

        return True

        # End

    def send_push_notification(self,
                               message=None,
                               message_type=None,
                               user_id=None, sender_obj_id=None):

        #  Get the aws arn from token table
        try:
            aws_token_data = AwsDeviceToken.objects.filter(
                user_id=user_id).latest("id")
        except AwsDeviceToken.DoesNotExist as e:
            logger.error(
                "Object Does Not Exist: AwsDeviceToken: {}, {}".format(
                    user_id, e))
            return False

        try:
            client = boto3.client('sns', **aws.AWS_CREDENTIAL)
        except Exception as e:
            logger.critical(
                "Caught Exception in {}, {}".format(
                    __file__, e))
            ravenclient.captureException()

        message = {
            'default': message,
            'APNS_SANDBOX': json.dumps({
                'aps': {
                    'alert': message,
                    'message_type': message_type,
                    "badge": 1,
                    "sound": "default"
                },
                'data': {
                    'sender_obj_id': sender_obj_id
                }})
        }
        message = json.dumps(message, ensure_ascii=False)
        print aws_token_data.aws_plateform_endpoint_arn
        # we will add except botocore.exceptions.ClientError as e:
        response = client.publish(
            TargetArn=str(aws_token_data.aws_plateform_endpoint_arn),
            Message=message,
            MessageStructure='json',
            MessageAttributes={
            }
        )
        return response

    @list_route(methods=['post'],)
    def invite_to_businesscard(self, request):
        user_id = request.user
        try:
            receiver_business_card_id = request.data[
                'receiver_business_card_id']
            sender_business_card_id = request.data['sender_business_card_id']
            get_profile = Profile.objects.filter(user_id=user_id).values(
                "first_name", "last_name").latest("id")
            user_name = str(get_profile["first_name"]) + \
                " " + str(get_profile["last_name"])
        except:
            return CustomeResponse(
                {
                    'msg': "Please provide receiver_business_card_id and sender_business_card_id"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
        # check from_business_card_id belongs to user_id
        try:
            sender_business_card = BusinessCard.objects.filter(
                user_id=user_id.id, id=sender_business_card_id).latest("id")
            receiver_business_card = BusinessCard.objects.filter(
                id=receiver_business_card_id).exclude(
                user_id=user_id.id).latest("id")
        except:
            return CustomeResponse(
                {
                    'msg': "Provided business cards are not correct"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

        request_type = 'b2b'
        receiver_obj_id = receiver_business_card_id
        message = 'request sent from ' + user_name + ' to accept businesscard.'
        # Before inser check request already sent
        already_sent_request = SendRequest.objects.filter(
            request_type=request_type,
            sender_user_id=user_id,
            sender_business_card_id=sender_business_card,
            receiver_user_id=receiver_business_card.user_id,
            receiver_bcard_or_contact_id=receiver_obj_id).exclude(
            request_status=2)

        # ----------------------- End------------------------ #
        if not already_sent_request:
            # send notification
            message = 'request sent from ' + user_name + ' to accept businesscard.'
            response = self.send_push_notification(
                message, 'b2b_invite', receiver_business_card.user_id.id)
            #  End
            # Insert into Notification Table
            insert_notification = self.insert_notification(
                request_type=request_type,
                sender_user_id=user_id,
                sender_business_card_id=sender_business_card,
                receiver_user_id=receiver_business_card.user_id,
                receiver_bcard_or_contact_id=receiver_obj_id,
                message=message)
            if insert_notification is not True:
                return CustomeResponse(
                    {
                        'msg': ""},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
        else:
            return CustomeResponse(
                {
                    'msg': "you have already sent request from your business card to other user business card"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

        # --------- End----------------------------------------------- #
        return CustomeResponse(response, status=status.HTTP_200_OK)

    # ---------- Receive Request ---------- #

    @list_route(methods=['post'],)
    def accept_businesscard(self, request):
        user_id = request.user
        try:
            receiver_business_card_id = request.data[
                'receiver_business_card_id']
            sender_business_card_id = request.data['sender_business_card_id']
            request_id = request.data['request_id']
        except:
            return CustomeResponse(
                {
                    'msg': "Please provide sender_business_card_id,receiver_business_card_id,request_id"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

        try:
            sender_business_card = BusinessCard.objects.select_related(
                "contact_detail").get(user_id=user_id.id, id=sender_business_card_id)
            receiver_business_card = BusinessCard.objects.select_related(
                "contact_detail").exclude(user_id=user_id.id).get(id=receiver_business_card_id)
        except:
            return CustomeResponse(
                {
                    'msg': "Provided business cards are not correct"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

        try:
            sender_folder = Folder.objects.get(
                businesscard_id=sender_business_card_id)
        except:
            return CustomeResponse(
                {
                    'msg': "sender businesscard dont have folder"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

        try:
            receiver_folder = Folder.objects.get(
                businesscard_id=receiver_business_card_id)
        except:
            return CustomeResponse(
                {
                    'msg': "receiver businesscard dont have folder"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

        # Now we are inserting data in folder contact table for making
        # connection
        exchange_business_cards = self.exchange_business_cards(
            sender_folder=sender_folder,
            sender_business_card=sender_business_card,
            receiver_folder=receiver_folder,
            receiver_business_card=receiver_business_card,
            sender_user_id=user_id)
        if exchange_business_cards is not True:
            return CustomeResponse(
                {
                    'msg': "Have some problem in exchangin businesscard"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
            logger.errors(
                "Have some problem in exchangin businesscard sender_business_card_id {},  receiver_business_card_id {} ".format(
                    sender_business_card_id, receiver_business_card_id))
        #  End

        else:
            #  Update the SendRequest status
            try:
                send_request_obj = SendRequest.objects.get(id=request_id)
                send_request_obj.request_status = 1
                send_request_obj.save()
            except SendRequest.DoesNotExist as e:
                logger.errors(
                    "Object Does Not Exist: SendRequest: {}, {}".format(
                        request_id, e))

            # send notification to receiver for acceptance business card
            user_name = str(receiver_business_card.user_id.user_profile.first_name) + \
                " " + str(receiver_business_card.user_id.user_profile.last_name)
            message = 'your business card accepted by ' + user_name
            self.send_push_notification(
                message,
                'b2b_accepted',
                receiver_business_card.user_id.id,
                sender_business_card.contact_detail.id)

            #  End
            return CustomeResponse(
                {"msg": "success"}, status=status.HTTP_200_OK)

    # cancel the invitation request
    @list_route(methods=['post'],)
    def cancel_invitation(self, request):
        user_id = request.user.id

        if 'request_id' in request.data:

            try:
                send_request_obj = SendRequest.objects.get(
                    receiver_user_id=user_id, id=request.data["request_id"])
                send_request_obj.request_status = 2
                send_request_obj.save()
            except SendRequest.DoesNotExist as e:
                logger.critical(
                    "cancel_invitation api : Object Does Not Exist: SendRequest: {}, {}".format(
                        request.data["request_id"], e))
                return CustomeResponse(
                    {
                        'msg': "request_id does not exist for this user"},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)

            return CustomeResponse(
                {"msg": "request cancelled successfully"}, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {
                    'msg': "Please provide request_id"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    # send white contact invitation
    @list_route(methods=['post'],)
    def send_white_invitation(self, request):

        try:
            data = {}
            user_id = request.user
            data['message'] = request.data.get('message')
            email = data['message']['email']
            user_exist = User.objects.filter(
                email=data['message']['email'])
        except:
            user_id = None
        if user_exist:
            logger.debug("email for grey contact already exists")
            return CustomeResponse(
                {
                    'msg': "email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
        else:
            try:
                sender_folder_id = FolderContact.objects.filter(
                    user_id=request.user.id, contact_id=request.data.get(
                        'receiver_bcard_or_contact_id')).values_list('folder_id', flat=True)[0]

                sender_business_card_id = Folder.objects.filter(
                    id=sender_folder_id).values_list(
                    'businesscard_id', flat=True)[0]

                data['email'] = request.user.email
                data['sender_user_id'] = request.user.id
                data['receiver_user_id'] = ''
                data['sender_business_card_id'] = sender_business_card_id
                data['request_type'] = "b2g"
                data['receiver_bcard_or_contact_id'] = request.data.get(
                    'receiver_bcard_or_contact_id')

                email = data['message']['email'].encode('base64', 'strict')
                fname = data['message']['fname'].encode('base64', 'strict')
                lname = data['message']['lname'].encode('base64', 'strict')
                contactId = str(data['receiver_bcard_or_contact_id']
                                ).encode('base64', 'strict')
                sid = str(data['sender_user_id']).encode('base64', 'strict')

            except:
                return CustomeResponse(
                    {
                        'msg': "Please provide receiver_bcard_or_contact_id"},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)

            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()[:10]
            email_invit_url = str(settings.DOMAIN_NAME) + "/api/greyrequest/invite_registration" + "/?email=" + \
                email + "&fname=" + fname + "&lname=" + \
                lname + "&cid=" + contactId + "&sid=" + sid

            serializer = SendRequestSerializer(
                data=data, context={'request': request, 'msg': 'not exist'})
            if serializer.is_valid():
                serializer.save()
                BaseSendMail.delay(
                    data,
                    type='grey_invitation',
                    key=activation_key,
                    url=email_invit_url,
                    first_name=fname,
                    email=email)
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(
                    {'msg': serializer.errors}, validate_errors=1)

        # yellow contacts
    @list_route(methods=['post'],)
    def rest_invitation(self, request):

        try:
            user_id = request.user.id
        except:
            user_id = None

        queryset_folder = SendRequest.objects.filter(
            receiver_obj_id=user_id, read_status=0).values()
        if queryset_folder:
            return CustomeResponse(
                {'msg': queryset_folder}, status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(
                {'msg': "data not found"}, validate_errors=1)


# needs to be optimized as per client provided form
class GreyInvitationViewSet(viewsets.ModelViewSet):

    queryset = SendRequest.objects.all()
    serializer_class = SendRequestSerializer

    @list_route(methods=['get'],)
    def invite_registration(self, request):
        try:
            email = request.GET.get('email').decode('base64', 'strict')
            fname = request.GET.get('fname').decode('base64', 'strict')
            lname = request.GET.get('lname').decode('base64', 'strict')
            cid = request.GET.get('cid').decode('base64', 'strict')
            sid = request.GET.get('sid').decode('base64', 'strict')
            domain_name = str(settings.DOMAIN_NAME)

        except:
            return CustomeResponse({'msg': "parameter(s) not found"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        return render(request,
                      'sendrequest/index.html',
                      {'email': email,
                       'fname': fname,
                       'lname': lname,
                       'cid': cid,
                       'sid': sid,
                       'domain_name': domain_name})
