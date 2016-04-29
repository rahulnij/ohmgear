# Third Party Imports
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import rest_framework.status as status
from rest_framework.decorators import list_route
from django.conf import settings
# Local app imports
from models import Group, GroupContacts, GroupMedia
from serializer import (
    GroupSerializer,
    GroupContactsSerializer,
    GroupMediaSerializer
)
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
from apps.businesscards.serializer import CountContactInBusinesscardSerializer
from apps.businesscards.models import BusinessCard
import logging
logger = logging.getLogger(__name__)

# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    """Group View."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """Create new group."""
        try:
            group_data = self.queryset.filter(user_id=request.user)
            try:
                if group_data:
                    serializer = self.serializer_class(group_data, many=True)
                    if serializer.data:
                        return CustomeResponse(
                            serializer.data, status=status.HTTP_200_OK)
            except Group.DoesNotExist:
                logger.error(
                    "Caught DoesNotExist exception for {}, user_id {},\
                    in {}".format(
                        self.__class__, user_id, __file__
                    )
                )
                return CustomeResponse(
                    {
                        "msg": "Group does not exist."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                    validate_errors=1
                )
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def create(self, request):
        """Create new group for a user."""
        try:
            newdata = request.data.copy()
            newdata['user_id'] = request.user.id
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
        except Exception:
            logger.critical("Caught Exception ", exc_info=True)
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def update(self, request, pk=None):
        """Update group details."""
        try:
            group_data = self.queryset.get(user_id=request.user.id, id=pk)
        except Group.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, primary key {},\
                in {}".format(
                    self.__class__, pk, __file__
                )
            )
            return CustomeResponse(
                {'msg': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        try:
            if group_data:
                group_updated_data = {}
                group_updated_data = request.data
                group_updated_data['user_id'] = request.user.id

                serializer = self.serializer_class(
                    group_data, data=group_updated_data)
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
        except Exception:
            logger.critical("Caught Exception ", exc_info=True)
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def deletegroups(self, request):
        """
        Delete multiple groups.

        If group is deleted than its contacts will also deleted.
        """
        try:
            user_id = request.user.id
            group_id = request.data['group_id']
        except KeyError:
            logger.error(
                "Caught KeyError exception: group_id \
                is required  , in {}".format(
                    __file__
                )
            )
            return CustomeResponse({'msg': 'group_id not found'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        group_data = self.queryset.filter(user_id=user_id, id__in=group_id)
        try:
            if group_data:
                group_data.delete()
                return CustomeResponse(
                    {'msg': 'group deleted successfully'}, status=status.HTTP_200_OK)
        except Exception:
            logger.critical("Caught Exception ", exc_info=True)
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def destroy(self, request, pk=None):
        """Delete not allowed as we can delete mutliple groups."""
        return CustomeResponse(
            {'msg': 'delete method not allowed'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['get'],)
    def getbusinesscardcarddetails(self, request):
        """
        Get all business cards of users with number of contacts in business created.

        Contacts Details also with count contacts in businesscards
        """
        try:
            user_id = request.user.id
        except KeyError:
            logger.error(
                "Caught KeyError exception: user.id \
                is required  , in {}".format(
                    __file__
                )
            )
            return CustomeResponse(
                {'msg': 'user not found'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        try:
            if user_id:
                queryset = BusinessCard.objects.filter(
                    user_id=request.user.id, status=1)

                serializer = CountContactInBusinesscardSerializer(
                    queryset, many=True, context={'request': user_id})
                return CustomeResponse(
                    serializer.data, status=status.HTTP_200_OK)

            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)

        except Exception:
            logger.critical("Caught Exception ", exc_info=True)
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )


class GroupContactsViewSet(viewsets.ModelViewSet):
    """Insert multiple Contacts in group."""

    queryset = GroupContacts.objects.all()
    serializer_class = GroupContactsSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permisssion_classes = IsAuthenticated

    def list(self, request):
        """List method not allowed in contacts."""
        return CustomeResponse({'msg': 'Get method bnot allowed'})

    def create(self, request):
        """Insert  mutliple Contacts in group."""
        try:
            user_id = request.user.id
            folder_contact_ids = request.data['folder_contact_id']
            group_id = request.data['group_id']
        except KeyError:
            logger.error(
                "Caught KeyError exception: folder_contact_id\
                is required  , in {}".format(
                    __file__
                )
            )
            return CustomeResponse({'msg': 'group contacts not found'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        try:
            temp_container = []
            for folder_contact_id in folder_contact_ids:
                group_contact_data_exist = self.queryset.filter(
                    user_id=request.user,
                    folder_contact_id=folder_contact_id,
                    group_id=group_id)
                if group_contact_data_exist:
                    return CustomeResponse(
                        {
                            'msg': 'contact is already added with this user'},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)

                temp_container.append({'folder_contact_id': folder_contact_id, 'group_id': group_id, 'user_id': user_id})
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
        except Exception:
            logger.critical("Caught Exception ", exc_info=True)
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def delete(self, request):
        """Delete mutliple Contacts in group."""
        try:
            user_id = request.user.id
            group_contact_id = request.data['group_contact_id']
        except KeyError:
            logger.error(
                "Caught KeyError exception: group_contact_id \
                is required  , in {}".format(
                    __file__
                )
            )
            return CustomeResponse({'msg': 'group contact id not found'},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        group_contact_data = self.queryset.filter(
            user_id=user_id, id__in=group_contact_id)
        try:
            if group_contact_data:
                group_contact_data.delete()
                return CustomeResponse(
                    {'msg': 'contact deleted successfully'}, status=status.HTTP_200_OK)
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )


# Adding group image in group


class GroupMediaViewSet(viewsets.ModelViewSet):
    """Insert group Image in group."""

    queryset = GroupMedia.objects.all()
    serializer_class = GroupMediaSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """List method not allowed."""
        return CustomeResponse({'msg': "list method not allowed"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def create(self, request):
        """Create method not allowed."""
        return CustomeResponse({'msg': "create method not allowed"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    # End
    # Upload image after group created
    @list_route(methods=['post'],)
    def upload(self, request):
        """Upload image for a group."""
        user_id = self.request.user.id
        try:
            group_id = self.request.data["group_id"]
        except KeyError:
            logger.error(
                "Caught KeyError exception, group_id not given in {} \
                by primary key {}".
                format(__file__, user_id)
            )
            return CustomeResponse({'msg': "provide group_id"},
                                   status=status.HTTP_400_BAD_REQUEST,
                                   validate_errors=1)
        try:
            group = Group.objects.get(id=group_id, user_id=user_id)
        except GroupMedia.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, primary key {},\
                in {}".format(
                    self.__class__, user_id, __file__
                )
            )
            return CustomeResponse({'msg': "Group id does not exist"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        #  Save Image in image Gallary
        media_exist = ''
        try:
            media_exist = GroupMedia.objects.get(group_id=group_id)
        except:
            pass

        try:
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
                except KeyError:
                    logger.error(
                        "Caught KeyError exception, password not given in {} \
                        by primary key {}".
                        format(__file__, user_id)
                    )
                    return CustomeResponse({'msg': "provide group_image"},
                                           status=status.HTTP_400_BAD_REQUEST,
                                           validate_errors=1)

                if data_new['group_image']:
                    return CustomeResponse({"group_id": group_id,
                                            "group_image": data_new['group_image']},
                                           status=status.HTTP_201_CREATED)
                else:
                    return CustomeResponse(
                        {
                            'msg': "Please upload media group_image or check whether it is already upload"},
                        status=status.HTTP_200_OK)
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

        # End

    # change image of group
    # change group image
    def update(self, request, pk=None):
        """Update group image old group image will be deleted."""
        try:
            group_data = self.queryset.get(
                user_id=request.user.id, group_id=pk)
        except GroupMedia.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, primary key {},\
                in {}".format(
                    self.__class__, user_id, __file__
                )
            )
            return CustomeResponse({'msg': 'Data not found'},
                                   status=status.HTTP_400_BAD_REQUEST,
                                   validate_errors=1)
        try:

            data = {}
            data['img_url'] = request.data['group_image']
            data['user_id'] = request.user.id
            data['group_id'] = pk

            if group_data:
                serializer = self.serializer_class(group_data, data=data)
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
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
        return CustomeResponse(
            {
                "msg": "Can not process request."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def destroy(self, request, pk):
        """Delete group image also deleted image from folder by signal."""
        try:
            user_id = request.user.id
            group_id = pk
        except KeyError:
            logger.error(
                "Caught KeyError exception, group_id not given in {} \
                by primary key {}".
                format(__file__, user_id)
            )
            return CustomeResponse(
                {
                    'msg': "Please provide correct group_id,"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
        try:

            get_image = GroupMedia.objects.get(
                group_id=group_id, user_id=user_id, status=1)
        except GroupMedia.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, primary key {},\
                in {}".format(
                    self.__class__, user_id, __file__
                )
            )
            return CustomeResponse(
                {
                    'msg': "Image not found"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
        try:
            if get_image:
                get_image.delete()
                return CustomeResponse(
                    {'msg': "Group image deleted successfully"}, status=status.HTTP_200_OK)
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
        return CustomeResponse(
            {
                'msg': "Please provide correct group_id,"},
            status=status.HTTP_400_BAD_REQUEST,
            validate_errors=1)
