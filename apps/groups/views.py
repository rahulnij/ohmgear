# Third Party Imports
from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
import rest_framework.status as status
from rest_framework.decorators import detail_route, list_route
from django.conf import settings
# Local app imports
from models import Group, GroupContacts, GroupMedia
from serializer import GroupSerializer, GroupContactsSerializer, GroupMediaSerializer
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        group_data = self.queryset.filter(user_id=request.user)
        try:
            serializer = self.serializer_class(group_data, many=True)
        except:
            return CustomeResponse(
                {
                    'msg': 'server error please try after some time'},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
        if serializer.data:
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg': 'Data not found for this user'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def create(self, request):

        # newdata = {}
        newdata = request.data.copy()
        newdata['user_id'] = request.user.id
        print newdata
        serializer = self.serializer_class(
            data=newdata, context={'request': request})
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return CustomeResponse(
                serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    def update(self, request, pk=None):
        try:
            group_data = self.queryset.get(user_id=request.user.id, id=pk)
        except:
            return CustomeResponse(
                {'msg': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        if group_data:
            serializer = self.serializer_class(group_data, data=request.data)
            print request.data
            print "request.data"
            if serializer.is_valid():
                serializer.save()
                return CustomeResponse(
                    serializer.data, status=status.HTTP_200_OK)
            else:
                return CustomeResponse(
                    serializer.errors, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg': 'Data cannot be updated'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        # try:
        #     group_data = self.queryset.filter(user_id=request.user.id, id=pk)
        #     print group_data
        #     print "group_data"
        #     print request.data['group_name']
        # except:
        #     return CustomeResponse(
        #         {'msg': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        # if group_data:
        #     group_data.update(group_name=request.data['group_name'])
        #     return CustomeResponse(
        #         {'msg': 'Data is updated'}, status=status.HTTP_200_OK)
        # else:
        #     return CustomeResponse({'msg': 'Data cannot be updated'},
        # status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    @list_route(methods=['post'],)
    def deletegroups(self, request):

        try:
            user_id = request.user.id
        except:
            user_id = ''

        try:
            group_id = request.data['group_id']
        except:
            return CustomeResponse({'msg': 'group_id not found'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        try:
            group_data = self.queryset.filter(user_id=user_id, id__in=group_id)
        except:
            return CustomeResponse(
                {'msg': 'group not found'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        if group_data:
            group_data.delete()
            return CustomeResponse(
                {'msg': 'group deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg': 'group cannot be deleted'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)


class GroupContactsViewSet(viewsets.ModelViewSet):
    queryset = GroupContacts.objects.all()
    serializer_class = GroupContactsSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permisssion_classes = IsAuthenticated

    def list(self, request):
        return CustomeResponse({'msg': 'Get method bnot allowed'})

    def create(self, request):

        try:
            user_id = request.user.id
        except:
            user_id = ''

        try:
            group_contacts = request.data['group_contacts']
        except:
            return CustomeResponse({'msg': 'group contacts not found'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        temp_container = []
        for contacts in group_contacts:
            data = {}
            data['folder_contact_id'] = contacts['folder_contact_id']
            data['group_id'] = contacts['group_id']
            data['user_id'] = user_id
            group_contact_data_exist = self.queryset.filter(
                user_id=request.user,
                folder_contact_id=data['folder_contact_id'],
                group_id=data['group_id'])
            if group_contact_data_exist:
                return CustomeResponse(
                    {
                        'msg': 'contact is already added with this user'},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)

            temp_container.append(data)

        serializer = self.serializer_class(
            data=temp_container, many=True, context={'contact_data': 1})
        if serializer.is_valid():
            serializer.save()
            return CustomeResponse(
                serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    @list_route(methods=['post'],)
    def delete(self, request):
        try:
            user_id = request.user.id
        except:
            user_id = ''

        try:
            group_contact_id = request.data['group_contact_id']
            print group_contact_id
        except:
            return CustomeResponse({'msg': 'group contact id not found'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        try:
            group_contact_data = self.queryset.filter(
                user_id=user_id, id__in=group_contact_id)

        except:
            return CustomeResponse({'msg': 'group contact data not found'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        if group_contact_data:
            group_contact_data.delete()
            return CustomeResponse(
                {'msg': 'contact deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {
                    'msg': 'contact cannot be deleted for this user'},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
# Adding group image in group


class GroupMediaViewSet(viewsets.ModelViewSet):
    queryset = GroupMedia.objects.all()
    serializer_class = GroupMediaSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # End
    # Upload image after group created
    @list_route(methods=['post'],)
    def upload(self, request):
        user_id = self.request.user.id
        try:
            group_id = self.request.data["group_id"]
        except:
            return CustomeResponse({'msg': "provide group_id"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        try:
            group = Group.objects.get(id=group_id, user_id=user_id)
        except:
            return CustomeResponse({'msg': "Group id does not exist"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        #  Save Image in image Gallary

        data_new = {}
        data_new['group_image'] = ""
        try:
            if 'group_image' in request.data and request.data[
                    'group_image']:

                group_image, created = GroupMedia.objects.update_or_create(
                    user_id=self.request.user, group_id=group, img_url=request.data['group_image'], status=1)
                data_new['group_image'] = str(
                    settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(group_image.img_url)
        except:
            pass

        if data_new['group_image']:
            return CustomeResponse({"group_id": group_id,
                                    "group_image": data_new['group_image']},
                                   status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(
                {
                    'msg': "Please upload media group_image"},
                status=status.HTTP_200_OK)
        # End

    #  Change image of group

    @list_route(methods=['post'],)
    def change(self, request):
        user_id = request.user.id
        try:
            contact_id = request.data["contact_id"]
            gallary_image_id = request.data["gallary_image_id"]
            # means it is 1 frontend or 2 backend
            image_type = request.data["image_type"]
        except:
            contact_id = None

        if contact_id:
            try:
                get_image = ContactMedia.objects.get(
                    id=gallary_image_id, contact_id=contact_id, user_id=user_id)
                print get_image
                get_image.status = 1
                get_image.front_back = image_type
                get_image.save()
                ContactMedia.objects.filter(
                    contact_id=contact_id,
                    front_back=image_type).exclude(
                    id=gallary_image_id).update(
                    status=0)
                return CustomeResponse(
                    {"msg": "Business card image changed successfully."}, status=status.HTTP_200_OK)
            except:
                return CustomeResponse(
                    {
                        'msg': "provided contact_id,gallary_image_id not valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
        else:
            return CustomeResponse(
                {
                    'msg': "Please provide contact_id,gallary_image_id"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
    # End

    def update(self, request, pk=None):
        return CustomeResponse({'msg': "Update method does not allow"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    @list_route(methods=['post'],)
    def delete(self, request):

        try:
            user_id = request.user.id
            contact_id = request.data["contact_id"]
            pk = request.data["media_id"]
            get_image = ContactMedia.objects.get(
                id=pk, contact_id=contact_id, user_id=user_id, status=1)
            get_image.delete()
            return CustomeResponse(
                {'msg': "Media deleted successfully"}, status=status.HTTP_200_OK)
        except:
            return CustomeResponse(
                {
                    'msg': "Please provide correct contact_id,media id"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
