# Third Party Imports
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status
from rest_framework.decorators import list_route
from django.conf import settings
# Local app imports
from models import Group, GroupContacts, GroupMedia
from serializer import GroupSerializer, GroupContactsSerializer, GroupMediaSerializer
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    """
    Create group.

    Create group with operations.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        Getting all group of a user.

        Getting all group of a user.
        """
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
        """
        Create new group for a user.

        Create new group for a user.
        """
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
        """
        Update group details.

        update group details.
        """
        try:
            group_data = self.queryset.get(user_id=request.user.id, id=pk)
        except:
            return CustomeResponse(
                {'msg': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        if group_data:
            serializer = self.serializer_class(group_data, data=request.data)
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

    @list_route(methods=['post'],)
    def deletegroups(self, request):
        """
        Delete multiple groups.

        If group is deleted than its Contacts will also deleted.
        """
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

    def destroy(self, request, pk=None):
        """
        Destroy method not allowed

        Delete not allowed as we can delete mutliple groups.
        """
        return CustomeResponse(
            {'msg': 'delete method not allowed'}, status=status.HTTP_400_BAD_REQUEST)


class GroupContactsViewSet(viewsets.ModelViewSet):
    """
    Insert Contacts in group.

    Insert multiple Contacts in group.
    """

    queryset = GroupContacts.objects.all()
    serializer_class = GroupContactsSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permisssion_classes = IsAuthenticated

    def list(self, request):
        """
        List method not allowed.

        List method not allowed in contacts.
        """
        return CustomeResponse({'msg': 'Get method bnot allowed'})

    def create(self, request):
        """
        Insert Contacts in group.

        Insert  mutliple Contacts in group
        """
        try:
            user_id = request.user.id
        except:
            user_id = ''
        try:
            group_contacts = request.data['folder_contact_id']
        except:
            return CustomeResponse({'msg': 'group contacts not found'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        temp_container = []
        for contacts in group_contacts:
            data = {}
            data['folder_contact_id'] = contacts
            data['group_id'] = request.data['group_id']
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
            data=temp_container, many=True)
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
        """
        Delete mutliple Contacts in group.

        Delete mutliple Contacts in group
        """
        try:
            user_id = request.user.id
        except:
            user_id = ''

        try:
            group_contact_id = request.data['group_contact_id']
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
    """
    Insert group Image in group.

    Insert group Image in group.
    """

    queryset = GroupMedia.objects.all()
    serializer_class = GroupMediaSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        List method not allowed.

        List method not allowed
        """
        return CustomeResponse({'msg': "list method not allowed"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def create(self, request):
        """
        Create method not allowed.

        Create method not allowed
        """
        return CustomeResponse({'msg': "create method not allowed"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    # End
    # Upload image after group created
    @list_route(methods=['post'],)
    def upload(self, request):
        """
        Upload image for a group.

        Upload image for a group.
        """
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
        media_exist = ''
        try:
            media_exist = GroupMedia.objects.get(group_id=group_id)
        except:
            pass
        if media_exist:
            return CustomeResponse({'msg': "GroupMedia already exist"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        else:

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
                        'msg': "Please upload media group_image or check whether it is already upload"},
                    status=status.HTTP_200_OK)
        # End

    # change image of group
    # change group image
    def update(self, request, pk=None):
        """
        Update group image

        old group image will be deleted from folder as well
        """
        try:
            group_data = self.queryset.get(
                user_id=request.user.id, group_id=pk)
            print group_data
            print "group_data"
        except:
            return CustomeResponse(
                {'msg': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        data = {}
        data['img_url'] = request.data['group_image']
        data['user_id'] = request.user.id
        data['group_id'] = pk

        if group_data:
            serializer = self.serializer_class(group_data, data=data)
            print serializer
            print "serializer"
            if serializer.is_valid():
                group_data.img_url.delete(False)
                serializer.save()
                return CustomeResponse(
                    serializer.data, status=status.HTTP_200_OK)
            else:
                return CustomeResponse(
                    serializer.errors, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg': 'Data cannot be updated'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def destroy(self, request, pk):
        """
        Delete group image.

        Also deleted image from folder by signal.
        """
        try:
            user_id = request.user.id
            group_id = pk
            get_image = GroupMedia.objects.get(
                group_id=group_id, user_id=user_id, status=1)
            print get_image
            print "get_image"
            get_image.delete()
            return CustomeResponse(
                {'msg': "Group image deleted successfully"}, status=status.HTTP_200_OK)
        except:
            return CustomeResponse(
                {
                    'msg': "Please provide correct group_id,"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
