"""Contact view set."""
#  Import Python Modules
import json
import validictory

# Third Party Imports
import rest_framework.status as status
from rest_framework.decorators import list_route
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import logging
from django.db import IntegrityError
from rest_framework.pagination import PageNumberPagination


# Application imports
from ohmgear.functions import CustomeResponse

from serializer import (
    ContactsSerializer,
    ContactsSerializerWithJson,
    FavoriteContactSerializer,
    AssociateContactSerializer,
    ContactMediaSerializer,
    PrivateContactSerializer,
    FolderContactWithDetailsSerializer,
    FolderContactWithRelatedDataSerializer
)


from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION
from models import (
    Contacts,
    FavoriteContact,
    AssociateContact,
    ContactMedia,
    PrivateContact
)
from ohmgear.token_authentication import ExpiringTokenAuthentication
from apps.businesscards.views import BusinessViewSet
from apps.folders.views import FolderViewSet
from apps.folders.models import Folder, FolderContact
from apps.folders.serializer import FolderContactSerializer
from permissions import IsUserContactData
import copy
from django.db.models import Q
import ohmgear.settings.constant as constant

logger = logging.getLogger(__name__)
ravenclient = getattr(settings, "RAVEN_CLIENT", None)
# End

# declaire the pagination class
class SetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

# Storing Contacts as a Bulk
# Note: we have to create same response format in this api in Second Phase
class storeContactsViewSet(viewsets.ModelViewSet):
    """Store contacts."""

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (
        IsAuthenticated,
        IsUserContactData,
    )

    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def list(self, request):
        """List store user's contacts."""
        try:
            queryset = FolderContact.objects.filter(
                user_id=request.user.id
            ).select_related()

            serializer = FolderContactWithDetailsSerializer(
                queryset,
                many=True
            )

            if serializer.data:
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        "msg": "No Data found"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=True
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def retrieve(self, request, pk=None):
        """Get contact by folder contact id."""
        try:
            queryset = FolderContact.objects.filter(contact_id=pk)
            serializer = FolderContactWithRelatedDataSerializer(
                queryset,
                many=True
            )
            if serializer.data:
                return CustomeResponse(
                    serializer.data, status=status.HTTP_200_OK)
            else:
                return CustomeResponse(
                    {
                        "msg": "No Data found"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=True
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def create(self, request):
        """Create not allowed."""
        return CustomeResponse(
            {
                'msg': 'POST method not allowed'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def uploads(self, request):
            """Upload bulk contacts."""
        # try:
            user_id = request.user
            NUMBER_OF_CONTACT = 100

            try:
                contact = request.data['contact']
            except KeyError:
                logger.error(
                    "Caught KeyError exception, contact not given in {}".
                    format(__file__)
                )
                return CustomeResponse(
                    {
                        'msg': 'Please provide correct Json Format'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
            counter = 0
            if contact:

                # Assign  first created business card to created default folder
                queryset_folder = Folder.objects.filter(
                    user_id=user_id, foldertype='PR').values()
                if not queryset_folder:
                    folder_view = FolderViewSet.as_view({'post': 'create'})
                    offline_data = {}
                    offline_data['businesscard_id'] = ''
                    offline_data['foldername'] = 'PR'
                    folder_view = folder_view(request, offline_data)
                    folder_id = folder_view.data['data']['id']
                else:
                    folder_id = queryset_folder[0]['id']

                contact_new = []
                for contact_temp in contact:
                    # Validate the json data
                    try:
                        validictory.validate(
                            contact_temp["bcard_json_data"],
                            BUSINESS_CARD_DATA_VALIDATION)
                    except validictory.ValidationError as error:
                        logger.error(
                            "Caught validictory.ValidationError\
                             exception, {} in {}".
                            format(error.message, __file__)
                        )
                        return CustomeResponse(
                            {
                                'msg': error.message
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                            validate_errors=1
                        )
                    except validictory.SchemaError as error:
                        logger.error(
                            "Caught validictory.SchemaError exception,\
                             {} in {}".
                            format(error.message, __file__)
                        )
                        return CustomeResponse(
                            {
                                'msg': error.message
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                            validate_errors=1
                        )

                if 'user_id' not in contact_temp:
                    contact_temp['user_id'] = user_id.id
                    contact_new.append(contact_temp)
                else:
                    contact_new.append(contact_temp)
                counter = counter + 1

            if counter > NUMBER_OF_CONTACT:
                return CustomeResponse(
                    {
                        'msg': "Max " + str(NUMBER_OF_CONTACT) +
                        " allowed to upload"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )

                if 'user_id' not in contact_temp:
                    contact_temp['user_id'] = user_id.id
                    contact_new.append(contact_temp)
                else:
                    contact_new.append(contact_temp)
                counter = counter + 1

                if counter > NUMBER_OF_CONTACT:
                    return CustomeResponse(
                        {
                            'msg': "Max " + str(NUMBER_OF_CONTACT) + " allowed to upload"},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)

            serializer = ContactsSerializer(data=contact_new, many=True)
            if serializer.is_valid():
                contact_data = serializer.save()
                #contact_id = contact_data[0].id

                # Assign all contacts to folder
                folder_contact_array = []
                contact_ids = []
                for items in serializer.data:
                    folder_contact_array.append(
                        {'user_id': user_id.id, 'folder_id': folder_id, 'contact_id': items['id']})
                    contact_ids.append(items['id'])

                if folder_contact_array:
                    folder_contact_serializer = FolderContactSerializer(
                        data=folder_contact_array, many=True)
                    if folder_contact_serializer.is_valid():
                        folder_contact_serializer.save()
                # End
                queryset = self.queryset.filter(
                    user_id=request.user.id,
                    businesscard_id__isnull=True,
                    id__in=contact_ids)
                serializer = ContactsSerializerWithJson(queryset, many=True)
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_201_CREATED)
        # except:
        #     logger.critical(
        #         "Caught exception in {}".format(__file__),
        #         exc_info=True
        #     )
        #     ravenclient.captureException()

        # return CustomeResponse(
        #     {
        #         "msg": "Can not process request. Please try later."
        #     },
        #     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     validate_errors=1
        # )

    def update(self, request, pk=None):
        data = request.data.copy()
        data['user_id'] = request.user.id
        try:
            folder_contact_data = FolderContact.objects.select_related(
                'contact_id').get(contact_id=pk, user_id=request.user.id)
            contact_data = folder_contact_data.contact_id
            link_status = folder_contact_data.link_status
            link_status_cons = constant.LINK_STATUS

            if link_status == link_status_cons.get(
                    'ORANGE') or link_status == link_status_cons.get('WHITE'):
                try:
                    validictory.validate(
                        request.data["bcard_json_data"],
                        BUSINESS_CARD_DATA_VALIDATION)
                except validictory.ValidationError as error:
                    return CustomeResponse(
                        {'msg': error.message},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
                except validictory.SchemaError as error:
                    return CustomeResponse(
                        {'msg': error.message},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
                except:
                    return CustomeResponse(
                        {
                            'msg': "Please provide bcard_json_data in \
                            json format"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)
                contact_serializer = ContactsSerializer(
                    contact_data, data=data, context={'request': request})
                if contact_serializer.is_valid():
                    contact_serializer.save()
                    data_new = contact_serializer.data.copy()
                else:
                    return CustomeResponse(
                        contact_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)

                return CustomeResponse(data_new, status=status.HTTP_200_OK)
            else:
                try:
                    newdata = {
                        "bcard_json_data": request.data["bcard_json_data"],
                        "foldercontact_id": folder_contact_data,
                        "user_id": request.user}
                except KeyError as e:
                    logger.error(
                        "KeyError in private contact update {}, {}".format(
                            __name__, e))
                    return CustomeResponse(
                        {
                            'msg': "Please provide bcard_json_data in \
                            json format"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)

                msg = self.privatecontact(newdata)
                return CustomeResponse({'msg': msg},
                                       status=status.HTTP_200_OK)
        except FolderContact.DoesNotExist as e:
            logger.error(
                "Object Does Not Exist: FolderContact-contact_update: \
                {}, {}".format(
                    pk, e
                )
            )
            return CustomeResponse(
                {
                    'msg': "FolderContact does not exist"
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    # Pending work remaining
    def privatecontact(self, newdata):
        """
        Private Contact contains additional contact_info.

        If there is connection with that contact.
        """
        # this update_or_create prone to race condition
        try:
            private_contact, created = PrivateContact.objects.update_or_create(
                newdata)
        except IntegrityError as e:
            logger.error(
                "IntegrityError at private contact update: {}, {}".format(
                    newdata['foldercontact_id'], e))

        if created:
            return 'additional information added successfully'
        else:
            return 'additional information updated successfully'

    @list_route(['post'],)
    def limitedaccess(self, request):
        """
        Limited Access to the contact will not get any update.

        Limited Access to the contact which is linked.
        """
        user_id = request.user.id
        link_status = constant.LINK_STATUS

        try:
            contact_id = request.data['contact_id']
        except KeyError:
            return CustomeResponse(
                {
                    'msg': 'contact_id not found'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            folder_contact_data = FolderContact.objects.filter(
                contact_id=contact_id, user_id=user_id)
            is_linked = folder_contact_data[0].is_linked
            if is_linked == 1:
                folder_contact_data.update(
                    link_status=link_status.get('BLUE'), is_linked=0)
                return CustomeResponse(
                    {
                        "msg": "Contact has limited_access now."
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        "msg": "Check your Contact is linked or not."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except IndexError:
            return CustomeResponse(
                {
                    'msg': 'Contact data not found'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def destroy(self, request, pk=None):
        """
        Destroy method will delete Contacts from Contact and folder_contact.

        if it is white contact ,other wise will be delete from  folder contact
        and that contact which is deleted having connection with cureent user
        then link_status will be change.
        """
        try:
            folder_contact_data = FolderContact.objects.select_related(
                'folder_id').get(contact_id=pk, user_id=request.user.id)
            link_status = folder_contact_data.link_status
            get_folder_data = folder_contact_data.folder_id
            get_user_bcard_id = get_folder_data.businesscard_id.id
            link_status_cons = constant.LINK_STATUS
        except FolderContact.DoesNotExist:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()
            return CustomeResponse(
                {
                    'msg': "Contact does not exists."
                },
                status=status.HTTP_404_NOT_FOUND,
                validate_errors=1
            )
        try:
            contact_data = Contacts.objects.filter(
                id=pk, user_id=request.user.id)

            if folder_contact_data:

                if link_status == link_status_cons.get(
                        'ORANGE') or link_status == link_status_cons.get('WHITE'):
                    if contact_data:
                        contact_data.delete()
                        return CustomeResponse(
                            {
                                'msg': "Contact has been deleted successfully"
                            },
                            status=status.HTTP_200_OK
                        )
                    else:
                        return CustomeResponse(
                            {
                                'msg': "Cannot be deleted"
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                            validate_errors=1
                        )

                else:
                    if link_status == link_status_cons.get('DELETED'):

                        try:
                            # find user contact_id with bcard_id and user_id
                            existing_contact_data = Contacts.objects.get(
                                businesscard_id=get_user_bcard_id,
                                user_id=request.user.id
                            )
                        except Contacts.DoesNotExist:
                            logger.critical(
                                "Caught exception in {}. Found contact_id {} in\
                                 foldercontact but not in contact.".format(__file__, pk),
                                exc_info=True
                            )
                            ravenclient.captureException()
                            return CustomeResponse(
                                {
                                    'msg': "Contact does not exists."
                                },
                                status=status.HTTP_404_NOT_FOUND,
                                validate_errors=1
                            )
                        # get contact id of user
                        getcontact_id = existing_contact_data.id
                        # get user_id of contact which is to be deleted.
                        existing_user_id = existing_contact_data.user_id
                        new_contact_data = Contacts.objects.get(
                            id=pk)

                        # new_contact_user_id = new_contact_data.id
                        if existing_user_id != new_contact_data.user_id.id and folder_contact_data:
                            new_user_folder_contact_data = FolderContact.objects.filter(
                                contact_id=getcontact_id, user_id=new_contact_data.user_id.id)
                            new_user_folder_contact_data.delete()
                            folder_contact_data.delete()
                            return CustomeResponse(
                                {
                                    'msg': "Both Connected Contact has been delete\
                                     successfully"
                                },
                                status=status.HTTP_200_OK
                            )

                        else:
                            return CustomeResponse(
                                {
                                    'msg': "Contact can not be deleted. try again"
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                                validate_errors=1)

                    else:
                        folder_contact_data = FolderContact.objects.filter(
                            contact_id=pk, user_id=request.user.id)
                        folder_contact_data.update(
                            link_status=link_status_cons.get('DELETED'),
                            is_linked=0
                        )
                        return CustomeResponse(
                            {
                                'msg': "Connected Contact has been deleted\
                                 successfully"
                            },
                            status=status.HTTP_200_OK
                        )

            else:
                return CustomeResponse(
                    {
                        'msg': "No contact found"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def merge_contacts(self, request):
        pass

    def find_duplicate(self, first_json, second_json):
        """Todo : check optimization."""
        try:
            first_name = []
            last_name = []
            email = []
            phone = []

            try:
                first_name = [value['value'] for value in first_json[
                    "side_first"]["basic_info"] if value['keyName'] == 'FirstName']
            except:
                pass

            try:
                last_name = [value['value'] for value in first_json[
                    "side_first"]["basic_info"] if value['keyName'] == 'LastName']
            except:
                pass

            try:
                email = [x['data'] for x in first_json[
                    "side_first"]["contact_info"]["email"]]
            except:
                pass

            try:
                phone = [x['data'] for x in first_json[
                    "side_first"]["contact_info"]["phone"]]
            except:
                pass
            # add second side data

            try:
                email = email + \
                    [x['data'] for x in first_json["side_second"]["contact_info"]["email"]]
            except:
                pass

            try:
                phone = phone + \
                    [x['data'] for x in first_json["side_second"]["contact_info"]["phone"]]
            except:
                pass

            first_name_target = []
            last_name_target = []
            email_target = []
            phone_target = []

            try:
                first_name_target = [value['value'] for value in second_json[
                    "side_first"]["basic_info"] if value['keyName'] == 'FirstName']
            except:
                pass

            try:
                last_name_target = [value['value'] for value in second_json[
                    "side_first"]["basic_info"] if value['keyName'] == 'LastName']
            except:
                pass

            # add second side data
            try:
                email_target = [x['data'] for x in second_json[
                    "side_first"]["contact_info"]["email"]]
            except:
                pass

            try:
                phone_target = [x['data'] for x in second_json[
                    "side_first"]["contact_info"]["phone"]]
            except:
                pass

            try:
                email_target = email_target + \
                    [x['data']
                        for x in second_json["side_second"]["contact_info"]["email"]]
            except:
                pass
            try:
                phone_target = phone_target + \
                    [x['data']
                        for x in second_json["side_second"]["contact_info"]["phone"]]
            except:
                pass
            # print email_target,phone_target
            check_duplicate_1 = 0
            for first_name_val in first_name:
                if first_name_val in first_name_target and first_name_val != []:
                    check_duplicate_1 = 1

            if not check_duplicate_1:
                for last_name_val in last_name:
                    if last_name_val in last_name_target and last_name_val != []:
                        check_duplicate_1 = 1

            check_duplicate_2 = 0
            for email_val in email:
                if email_val in email_target and email_val != []:
                    check_duplicate_2 = 1

            if not check_duplicate_2:
                for phone_val in phone:
                    if phone_val in phone_target and phone_val != []:
                        check_duplicate_2 = 1

            # Condition {First_Name OR Last_Name} AND {email OR phone OR instant_message}
            # print check_duplicate_1,check_duplicate_2
            if check_duplicate_1 and check_duplicate_2:
                return 1
            else:
                return 0
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def get_duplicate_contacts(self, request):
        """Not in use as duplicate task will be done at device side."""
        try:
            user_id = request.user.id
            contacts = list(self.queryset.filter(user_id=user_id).values(
                'id', 'businesscard_id', 'bcard_json_data').order_by("id"))
            contacts_copy = contacts
            # fetch contact json detail from qeuryset

            finalContacts = []
            count = 0
            duplicate_contacts_ids = []
            inner_loop = 0

            for value in contacts:
                check = 1
                duplicateContacts = []
                iterator = iter(contacts_copy)
                try:
                    while True:
                        value_copy = iterator.next()

                        if value["id"] != value_copy["id"] and value[
                                "id"] not in duplicate_contacts_ids:
                            result = self.find_duplicate(
                                value["bcard_json_data"], value_copy["bcard_json_data"])
                            if result:
                                if check == 1:
                                    finalContacts.append(value)
                                    inner_loop = inner_loop + 1
                                    check = 0
                                duplicateContacts.append(
                                    json.loads(json.dumps(value_copy)))
                                duplicate_contacts_ids.append(value_copy["id"])
                except StopIteration as e:
                    if count == inner_loop - 1:
                        finalContacts[inner_loop -
                                      1]["duplicate"] = duplicateContacts
                        count = count + 1

            return CustomeResponse(finalContacts, status=status.HTTP_200_OK)
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def merge(self, request):
        """Merge contacts."""
        try:
            user_id = request.user.id
        except:
            user_id = None
        try:
            merge_contact_ids = request.data["merge_contact_ids"]
            target_contact_id = request.data["target_contact_id"]
        except KeyError:
            return CustomeResponse(
                {
                    "msg": "Please provide merge_contact_ids,\
                     target_contact_id"
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        # Get the  target_bcard_id and merge_bcards_ids data
        try:
            target_contact = Contacts.objects.get(
                id=target_contact_id, user_id=user_id)

            first_json = json.loads(json.dumps(target_contact.bcard_json_data))

            # make sure target_bcard_id not in merge_bcards_ids
            if target_contact_id not in merge_contact_ids:

                merge_contacts = Contacts.objects.filter(
                    id__in=merge_contact_ids, user_id=user_id).exclude(
                    businesscard_id__isnull=False).all()
                if merge_contacts:
                    # pass

                    for temp in merge_contacts:
                        contact_json_data = temp.bcard_json_data
                        if contact_json_data:
                            try:
                                second_json = json.loads(
                                    json.dumps(contact_json_data))
                            except:
                                second_json = {}
                            third_json = second_json.copy()
                            card_object = BusinessViewSet()
                            card_object.mergeDict(third_json, first_json)

                            # assign the new json
                            target_contact.bcard_json_data = third_json
                            target_contact.save(force_update=True)
                            first_json = third_json
                    merge_contacts.delete()
                    return CustomeResponse(
                        {
                            "msg": "successfully merged"
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return CustomeResponse(
                        {
                            "msg": "merge_contact_ids does not exist OR merge\
                             contact links with business card"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )

            else:
                return CustomeResponse(
                    {
                        "msg": "Please provide correct target_contact_id"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except Contacts.DoesNotExist:
            return CustomeResponse(
                {
                    "msg": "target_contact_id does not exist"
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    # Favorite Contact

    @list_route(methods=['post'],)
    def addFavoriteContact(self, request):
        """Add favorite contact."""
        try:
            contact_id = request.data['foldercontact_id']
        except KeyError:
            return CustomeResponse(
                {
                    'msg': 'foldercontact_id not found'
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

#        data['user_id'] = request.user.id
        tempContainer = []
        for data in contact_id:
            tempData = {}
            tempData['user_id'] = request.user.id
            tempData['foldercontact_id'] = data
            tempContainer.append(tempData)

        try:
            serializer = FavoriteContactSerializer(
                data=tempContainer,
                context={'request': request},
                many=True
            )

            if serializer.is_valid():
                serializer.save()
            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

            return CustomeResponse(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    # Get all favorite contact of a user

    @list_route(methods=['get'],)
    def getFavoriteContact(self, request):
        """Get favorite contacts."""
        user_id = request.user.id
        try:
            favoriteContactData = FavoriteContact.objects.filter(
                user_id=user_id)
            if favoriteContactData:
                serializer = FavoriteContactSerializer(
                    favoriteContactData,
                    many=True
                )
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': 'favorite contact not found for this user'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def deleteFavoriteContact(self, request):
        """Delete favorite Contact."""
        user_id = request.user.id
        try:
            foldercontact_id = request.data['foldercontact_id']
        except KeyError:
            return CustomeResponse(
                {
                    'msg': 'Folder Contact_id is required.'
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        try:
            favoriteContactData = FavoriteContact.objects.filter(
                user_id=user_id, foldercontact_id__in=foldercontact_id)
            if favoriteContactData:
                favoriteContactData.delete()
                return CustomeResponse(
                    {
                        'msg': 'Deleted favorite contact.'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': 'Favorite Contact cannot be deleted'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def addAssociateContact(self, request):
        """
        Associate Contact.

        Insert Associate Contact it will be 2 way process
        """
        user_id = request.user.id

        try:
            associate_from = request.data['associate']
            associate_to = request.data['associate_to']

            # use copy.deepcopy main request.data will be same otherwise it
            # will be override by all_contact
            all_contact = copy.deepcopy(request.data['associate_to'])

            all_contact.append(associate_from)

        except KeyError:
            return CustomeResponse(
                {
                    'msg': 'Please Check json format'
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        try:
            associate_contact = FolderContact.objects.filter(
                user_id=user_id, id__in=all_contact).values()
            user_contact = []
            for data in associate_contact:
                contact = {}
                contact = data['id']
                user_contact.append(contact)

            if associate_from in user_contact:
                # intersect Associate_from and user_contact
                associate_contact = list(set(user_contact) & set(associate_to))
                if not associate_contact:
                    return CustomeResponse(
                        {
                            'msg': 'Associate Contact is not there'
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1
                    )
                tempContainer = []

                for contact in associate_contact:
                    tempData = {}
                    newdata = {}
                    tempData['associatefoldercontact_id'] = associate_from
                    tempData['foldercontact_id'] = contact
                    tempData['user_id'] = request.user.id

                    newdata['associatefoldercontact_id'] = contact
                    newdata['foldercontact_id'] = associate_from
                    newdata['user_id'] = request.user.id

                    tempContainer.append(tempData)
                    tempContainer.append(newdata)

                serializer = AssociateContactSerializer(
                    data=tempContainer, many=True)
                if serializer.is_valid():
                    serializer.save()
                    return CustomeResponse(
                        serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return CustomeResponse(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)

            else:
                return CustomeResponse(
                    {
                        'msg': 'The contact from which to associate is not\
                         in user Contact'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'])
    def getAssociateContact(self, request):
        """Get All associate Contact of a user."""
        try:
            associate_folder_id = request.data['associatefoldercontact_id']
        except KeyError:
            logger.error(
                "Caught KeyError exception, in {}".
                format(__file__)
            )
            return CustomeResponse(
                {
                    'msg': 'associatefoldercontact_id is required.'
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        try:
            accociateContactData = AssociateContact.objects.filter(
                associatefoldercontact_id=associate_folder_id
            )

            if accociateContactData:
                serializer = AssociateContactSerializer(
                    accociateContactData, many=True)
                return CustomeResponse(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': 'Assciate Contact not found'
                    },
                    status=status.HTTP_404_NOT_FOUND,
                    validate_errors=1
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'])
    def deleteAssociateContact(self, request):
        """Delete Associate Contact to whom it is connected."""
        user_id = request.user.id

        try:
            associate_from = request.data['associate_from']
            associate_to = request.data['associate_to']

        except KeyError:
            return CustomeResponse(
                {
                    'msg': 'Associate Contact not found'
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        try:
            associateContactData = AssociateContact.objects.filter(
                Q(
                    user_id=user_id,
                    associatefoldercontact_id__in=associate_from,
                    foldercontact_id__in=associate_to) | Q(
                    user_id=user_id,
                    associatefoldercontact_id__in=associate_to,
                    foldercontact_id__in=associate_from)
            )

            if associateContactData:
                associateContactData.delete()
                return CustomeResponse(
                    {
                        'msg': 'Associate Contact delete successfully'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': 'Assciate Contact cannot be deleted'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def upload_contact_profile(self, request):
        """Upload profile image for a contact."""

        try:
            contact_profile_image = request.data['contact_profile_image']
            user_id = request.user.id
            contact_id = request.data['contact_id']
            contact_data = self.queryset.get(
                user_id=user_id,
                id=contact_id
            )
            data = {}
            data_new = {}
            data['contact_profile_image'] = contact_profile_image
            data['user_id'] = user_id
            data['contact_id'] = contact_id

            if contact_data:
                contact_profile_image = request.data['contact_profile_image']
                data_new['contact_profile_image'] = str(
                    settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(contact_profile_image)
                serializer = self.serializer_class(contact_data, data=data)
                if serializer.is_valid():
                    contact_data.contact_profile_image.delete(False)
                    serializer.save()
                    return CustomeResponse({
                        "contact_id": contact_id,
                        "contact_profile_image": data_new['contact_profile_image']
                    }, status=status.HTTP_200_OK)
                else:
                    return CustomeResponse(
                        serializer.errors, status=status.HTTP_200_OK)
            else:
                return CustomeResponse(
                    {
                        'msg': 'Contact Profile Image cannot be uploaded'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1
                )
        except Contacts.DoesNotExist:
            logger.error(
                "Caught DoesNotExist exception for {}, primary key {},\
                in {}".format(
                    Contacts.__name__, user_id, __file__
                )
            )
            return CustomeResponse(
                {
                    'msg': 'Contact not found'
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except Exception:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()
        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )


class ContactMediaViewSet(viewsets.ModelViewSet):
    """Contact Images Upload."""

    queryset = ContactMedia.objects.all().order_by('front_back')
    serializer_class = ContactMediaSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        user_id = self.request.user.id
        try:
            contact_id = self.request.data['contact_id']
        except KeyError:
            return CustomeResponse(
                {
                    'msg': 'contact_id is required.'
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        try:
            self.queryset = self.queryset.filter(
                contact_id=contact_id,
                user_id=user_id
            )
            if self.queryset:
                data = {}
                data['all'] = []
                data['top'] = []
                for items in self.queryset:
                    if items.status == 1:
                        data['top'].append({"image_id": items.id, "front_back": items.front_back, "img_url": str(
                            settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(items.img_url)})
                    data['all'].append({"image_id": items.id, "front_back": items.front_back, "img_url": str(
                        settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(items.img_url)})
                return CustomeResponse(
                    data,
                    status=status.HTTP_200_OK
                )
            else:
                return CustomeResponse(
                    {
                        'msg': "Contact images does not exist."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                    validate_errors=1
                )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()

        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    def create(self, request, call_from_function=None):
        """
        Add image into business card gallery.

        return CustomeResponse({"msg":"POST method not
        allowed"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        """
        data = request.data.copy()
        data['status'] = 0
        data['user_id'] = self.request.user.id
        try:
            serializer = ContactMediaSerializer(
                data=data,
                context={
                    'request': request
                }
            )

            if serializer.is_valid():
                serializer.save()
                if call_from_function:
                    return json.loads(unicode(serializer.data))
                else:
                    return CustomeResponse(
                        serializer.data, status=status.HTTP_201_CREATED)
            else:
                if call_from_function:
                    return serializer.errors
                else:
                    return CustomeResponse(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()
        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def upload(self, request):
        user_id = self.request.user.id
        try:
            contact_id = self.request.data["contact_id"]
        except KeyError:
            logger.error(
                "Caught KeyError exception, in {}".
                format(__file__),
                exc_info=True
            )
            return CustomeResponse(
                {
                    'msg': "contact_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        try:
            contact = Contacts.objects.get(id=contact_id, user_id=user_id)
        except Contacts.DoesNotExist:
            return CustomeResponse(
                {
                    'msg': "Contact id does not exist."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        #  Save Image in image Gallary

        data_new = {}
        data_new['bcard_image_frontend'] = ""
        data_new['bcard_image_backend'] = ""
        try:
            try:
                if 'bcard_image_frontend' in request.data and request.data[
                        'bcard_image_frontend']:

                    #  Set previous image 0
                    ContactMedia.objects.filter(
                        contact_id=contact, front_back=1).update(status=0)
                    bcard_image_frontend, created = ContactMedia.objects.update_or_create(
                        user_id=self.request.user,
                        contact_id=contact,
                        img_url=request.data['bcard_image_frontend'],
                        front_back=1,
                        status=1
                    )
                    data_new['bcard_image_frontend'] = str(
                        settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(bcard_image_frontend.img_url)
            except:
                pass

            try:
                if 'bcard_image_backend' in request.data and request.data[
                        'bcard_image_backend']:
                    ContactMedia.objects.filter(
                        contact_id=contact, front_back=2).update(status=0)
                    bcard_image_backend, created = ContactMedia.objects.update_or_create(
                        user_id=self.request.user,
                        contact_id=contact,
                        img_url=request.data['bcard_image_backend'],
                        front_back=2, status=1
                    )
                    if bcard_image_backend:
                        data_new['bcard_image_backend'] = str(
                            settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(bcard_image_backend.img_url)

            except:
                pass

            if data_new['bcard_image_frontend'] or data_new[
                    'bcard_image_backend']:
                return CustomeResponse({"contact_id": contact_id,
                                        "bcard_image_frontend": data_new['bcard_image_frontend'],
                                        "bcard_image_backend": data_new['bcard_image_backend']},
                                       status=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(
                    {
                        'msg': "Please upload media bcard_image_frontend or\
                         bcard_image_backend"},
                    status=status.HTTP_200_OK)
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()
        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def change(self, request):
        """Change image of business card."""
        user_id = request.user.id
        try:
            contact_id = request.data["contact_id"]
            gallary_image_id = request.data["gallary_image_id"]
            # means it is 1 frontend or 2 backend
            image_type = request.data["image_type"]
        except KeyError:
            logger.error(
                "Caught KeyError exception, in {}.".
                format(__file__),
                exc_info=True
            )
            return CustomeResponse(
                {
                    'msg': "Please provide contact_id,gallary_image_id."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )

        try:
            get_image = ContactMedia.objects.get(
                id=gallary_image_id,
                contact_id=contact_id,
                user_id=user_id
            )
            get_image.status = 1
            get_image.front_back = image_type
            get_image.save()
            ContactMedia.objects.filter(
                contact_id=contact_id,
                front_back=image_type).exclude(
                id=gallary_image_id).update(
                status=0)
            return CustomeResponse(
                {
                    "msg": "Business card image changed successfully."
                },
                status=status.HTTP_200_OK
            )
        except:
            logger.critical(
                "Caught exception in {}".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()
        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )

    # End

    def update(self, request, pk=None):
        """Update not allowed."""
        return CustomeResponse(
            {
                'msg': "Update method does not allow."
            },
            status=status.HTTP_400_BAD_REQUEST,
            validate_errors=1
        )

    @list_route(methods=['post'],)
    def delete(self, request):
        """Delete Contact media."""
        try:
            user_id = request.user.id
            contact_id = request.data["contact_id"]
            pk = request.data["media_id"]
            get_image = ContactMedia.objects.get(
                id=pk, contact_id=contact_id, user_id=user_id, status=1)
            get_image.delete()
            return CustomeResponse(
                {
                    'msg': "Media deleted successfully."
                },
                status=status.HTTP_200_OK
            )
        except KeyError:
            return CustomeResponse(
                {
                    'msg': "Please provide correct contact_id,media id."
                },
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1
            )
        except ContactMedia.DoesNotExist:
            return CustomeResponse(
                {
                    'msg': 'ContactMedia not found.'
                },
                status=status.HTTP_404_NOT_FOUND,
                validate_errors=1
            )
        except:
            logger.critical(
                "Caught exception in {}.".format(__file__),
                exc_info=True
            )
            ravenclient.captureException()
        return CustomeResponse(
            {
                "msg": "Can not process request. Please try later."
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            validate_errors=1
        )
