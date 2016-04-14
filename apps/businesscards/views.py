# --------- Import Python Modules ----------- #
import json
import validictory
import collections
# ------------------------------------------- #
# ------------ Third Party Imports ---------- #
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import rest_framework.status as status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import list_route
from django.core.exceptions import ObjectDoesNotExist
# ------------------------------------------- #
# ----------------- Local app imports ------ #
from models import BusinessCard, BusinessCardTemplate, BusinessCardIdentifier, Identifier, BusinessCardSkillAvailable, BusinessCardAddSkill, BusinessCardHistory
from serializer import BusinessCardSerializer, BusinessCardIdentifierSerializer, BusinessCardSkillAvailableSerializer, BusinessCardAddSkillSerializer, BusinessCardSummarySerializer, BusinessCardHistorySerializer
from apps.contacts.serializer import ContactsSerializer
from apps.contacts.models import Contacts, ContactMedia
from apps.identifiers.serializer import BusinessIdentifierSerializer
from ohmgear.token_authentication import ExpiringTokenAuthentication
from ohmgear.functions import CustomeResponse, rawResponse
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION
from apps.users.models import User
from apps.vacationcard.models import VacationCard
from apps.folders.views import FolderViewSet
from apps.sendrequest.views import SendAcceptRequest
from apps.folders.models import Folder, FolderContact
from apps.folders.serializer import FolderSerializer
from serializer import BusinessCardWithIdentifierSerializer
import re
# ---------------------------End------------- #


# ---------------- Business Card Summary ---------------------- #
class CardSummary(APIView):
    """
    View to card summary.
    """
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = BusinessCard.objects.all()

    def get(self, request):
        bcard_id = self.request.QUERY_PARAMS.get('bcard_id', None)
        if bcard_id:
            queryset = self.queryset.filter(id=bcard_id)

            serializer = BusinessCardSummarySerializer(queryset, many=True)
            dt = serializer.data
            for d in serializer.data:
                dt = d
                businesscard = BusinessCard(id=bcard_id)
#                dt['business_media'] =  businesscard.bcard_image_frontend()
                break
            return CustomeResponse(dt, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {
                    'msg': 'GET method not allowed without business card id'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
                validate_errors=1)

    def post(self, request, format=None):
        return CustomeResponse({'msg': 'POST method not allowed'},
                               status=status.HTTP_405_METHOD_NOT_ALLOWED,
                               validate_errors=1)
# ---------------------- End ---------------------------------- #


# Create your views here.

class BusinessCardIdentifierViewSet(viewsets.ModelViewSet):
    queryset = BusinessCardIdentifier.objects.all()
    serializer_class = BusinessCardIdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # --------------Method: GET----------------------------- #

    def list(self, request):

        user_id = request.user
        self.queryset = Identifier.objects.all().filter(user_id=user_id)
        """
            get all identifiers from identifiers table
            """
        serializer = BusinessIdentifierSerializer(self.queryset, many=True)
        if serializer:
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {'msg': "No Data Found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def create(self, request, call_from_function=None, offline_data=None):
        try:
            op = request.data['op']
        except:
            op = None
        if op == 'change':
            businesscard_id = request.data['businesscard_id']

            if businesscard_id:
                businesscardidentifier_detail = BusinessCardIdentifier.objects.filter(
                    businesscard_id=businesscard_id)
                businesscardidentifier_detail.delete()

        # TODO check business card and identifier belongs to authentic user
        # --------- END ----- #
        data = {}
        if call_from_function:
            data = offline_data
        else:
            data = request.data
        serializer = BusinessCardIdentifierSerializer(
            data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            BusinessCard.objects.filter(
                id=data['businesscard_id']).update(status=1, is_active=1)
            if call_from_function:
                return rawResponse(
                    serializer.data,
                    status=True,
                    status_code=status.HTTP_201_CREATED)
            else:
                return CustomeResponse(
                    serializer.data, status=status.HTTP_201_CREATED)
        else:
            if call_from_function:
                return rawResponse(serializer.errors)
            else:
                return CustomeResponse(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)

    @list_route(methods=['post'],)
    def unlinkIdentifier(self, request):

        identifier_id = request.data['identifier_id']
        businesscard_id = request.data['bcard_id']
        getbusinessacard_identifier_data = BusinessCardIdentifier.objects.filter(
            identifier_id=identifier_id, businesscard_id=businesscard_id)

        # ------Unlink Businesscard Identifier status 0 in Bsuinesscardidentifier table-------- #
        if getbusinessacard_identifier_data:
            getbusinessacard_identifier_data.delete()
            return CustomeResponse(
                {'msg': "Business card has been unlinked with identifiers "}, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg': "Card is not attached"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    # -------Delete Identifiers it will first inactive the businesscard than delete the linking of identifier with businesscard in businesscard_identifier table
    # than delete the identifeirs in identifier table ------------ #
    def destroy(self, request, pk=None):

        identifier_data = Identifier.objects.filter(id=pk)

        if identifier_data:
            businesscard_identifier_data = BusinessCardIdentifier.objects.filter(
                identifier_id=identifier_data)
            if businesscard_identifier_data:

                businesscard_id = businesscard_identifier_data[
                    0].businesscard_id.id
                BusinessCard.objects.filter(
                    id=businesscard_id).update(status=0, is_active=0)
                businesscard_identifier_data.delete()
            identifier_data.delete()
            return CustomeResponse(
                {
                    'msg': "Business card has been Inactive and identifiers has been deleted "},
                status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {
                    'msg': "Businesscard Identifier Id not found"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    # -----------------search contact by identifier ------------ #

    @list_route(methods=['post'])
    def searchIdentifier(self, request):
        from functions import searchjson
        try:
            user_id = request.user.id

        except:
            user_id = ''
            return CustomeResponse(
                {'msg': "user not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        try:
            value = request.data['name']
        except:
            value = ''
            return CustomeResponse({'msg': "Please provide name"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

        if (' ' in value) == True:
            name = "firstname_lastname"
            user_id = ''
            data = searchjson(name, value)

        else:

            if not re.match("[^@]+@[^@]+\.[^@]+", value):

                name = "identifier"
                try:
                    identifier_data = Identifier.objects.filter(
                        identifier=value, status=1)

                except:
                    return CustomeResponse(
                        {'msg': "Server error"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

                if not identifier_data:
                    return CustomeResponse(
                        {'msg': "identifier not Found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

                serializer = BusinessIdentifierSerializer(
                    identifier_data, many=True)

                try:
                    businesscard_data = serializer.data[
                        0]['business_identifier']
                    contact_id = serializer.data[0][
                        'business_identifier'][0]['contact_detail']['id']
                except:
                    return CustomeResponse(
                        {'msg': "No Business card found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
                try:
                    folder_contacts = FolderContact.objects.filter(
                        user_id=user_id, contact_id=contact_id)
                except:
                    return CustomeResponse(
                        {'msg': "server error"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

                if folder_contacts:
                    return CustomeResponse(
                        {
                            'msg': "Business card is already been added"},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)
                else:

                    if businesscard_data:

                        if businesscard_data[0]['status']:
                            return CustomeResponse(
                                serializer.data, status=status.HTTP_200_OK)
                        else:
                            return CustomeResponse(
                                {
                                    'msg': "Business Card is not published"},
                                status=status.HTTP_400_BAD_REQUEST,
                                validate_errors=1)

                    else:
                        return CustomeResponse(
                            {'msg': "No Business Card Found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

            else:
                try:
                    userdata = User.objects.filter(email=value).values()
                except:
                    return CustomeResponse(
                        {'msg': "Server error"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
                if userdata:
                    print "userdata email"
                    user_id = userdata[0]['id']
                    name = "email"
                    data = searchjson(name, value, user_id)
                    if data:
                        serializer = BusinessCardWithIdentifierSerializer(
                            data, many=True)
                        return CustomeResponse(
                            serializer.data, status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse(
                            {'msg': "email not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
#
                else:
                    name = "email"
                    user_id = ""
                    data = searchjson(name, value)
                    if data:
                        serializer = BusinessCardWithIdentifierSerializer(
                            data, many=True)
                        return CustomeResponse(
                            serializer.data, status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse(
                            {'msg': "email not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

# BusinessCard History


class BusinessCardHistoryViewSet(viewsets.ModelViewSet):
    queryset = BusinessCardHistory.objects.all()
    serializer_class = BusinessCardHistorySerializer

    def list(self, request):

        bid = self.request.QUERY_PARAMS.get('bid', None)
        if bid:
            self.queryset = self.queryset.filter(
                businesscard_id=bid).order_by('updated_date').values()

            if self.queryset:
                data = {}
                data['side_first'] = []
                data['side_second'] = []

                # for items in self.queryset:
                #   data['side_first'].append({"bcard_json_data":items['bcard_json_data']['side_first']['basic_info']})
                #  data['side_second'].append({"bcard_json_data":items['bcard_json_data']['side_second']['contact_info']})
        serializer = self.serializer_class(self.queryset, many=True)
        if serializer:
            return CustomeResponse(self.queryset, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    def create(self, request):
        serializer = BusinessCardHistorySerializer(
            data=request.data, context={'request': request})
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

    def update(self, request, pk=None):
        return CustomeResponse({'msg': "Update method does not allow"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

# BusinessCard Available Skills


class BusinessCardSkillAvailableViewSet(viewsets.ModelViewSet):
    queryset = BusinessCardSkillAvailable.objects.all()
    serializer_class = BusinessCardSkillAvailableSerializer

    def list(self, request):
        skill = self.request.QUERY_PARAMS.get('skill', None)
        if skill:
            self.queryset = self.queryset.filter(skill_name__istartswith=skill)
        serializer = self.serializer_class(self.queryset, many=True)
        if serializer and self.queryset:
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(
                {'msg': 'no data found'}, status=status.HTTP_200_OK, validate_errors=1)

    def create(self, request):
        serializer = BusinessCardSkillAvailableSerializer(
            data=request.data, context={'request': request})
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

    def update(self, request, pk=None):
        return CustomeResponse({'msg': "Update method does not allow"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    @list_route(methods=['get'],)
    def allSkills(self, request):
        try:
            skillsAvailable = BusinessCardSkillAvailable.objects.all()
            serializer = BusinessCardSkillAvailableSerializer(
                skillsAvailable, many=True)
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        except:
            return CustomeResponse({"msg": "email is mandatory"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    # Add Skills to Business Card


class BusinessCardAddSkillViewSet(viewsets.ModelViewSet):

    queryset = BusinessCardAddSkill.objects.all()
    serializer_class = BusinessCardAddSkillSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # --------------Method: GET----------------------------- #

    def list(self, request):
        return CustomeResponse({'msg': 'GET method not allowed'},
                               status=status.HTTP_405_METHOD_NOT_ALLOWED,
                               validate_errors=1)

    def retrieve(self, request, pk=None):
        return CustomeResponse({'msg': 'GET method not allowed'},
                               status=status.HTTP_405_METHOD_NOT_ALLOWED,
                               validate_errors=1)

    def create(self, request):
        tempData = {}
        tempData['user_id'] = request.user.id
        tempData['businesscard_id'] = request.data['businesscard_id']
        tempData['skill_name'] = request.data['skill_name'].split(',')
        serializer = BusinessCardAddSkillSerializer(
            data=tempData, context={'request': request})

        if serializer.is_valid():
            businesscard_id = tempData['businesscard_id']
            user_id = tempData['user_id']
            skill_name = tempData['skill_name']

            BusinessCardAddSkill.objects.filter(
                businesscard_id=businesscard_id).delete()
            for item in skill_name:
                data = {}
                data['skill_name'] = item
                data['user_id'] = user_id
                data['businesscard_id'] = businesscard_id
                serializer = BusinessCardAddSkillSerializer(
                    data=data, context={'request': request})
                serializer.is_valid()
                serializer.save()
            return CustomeResponse(
                serializer.data,
                status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    def update(self, request, pk=None):
        return CustomeResponse({'msg': "Update method does not allow"},
                               status=status.HTTP_400_BAD_REQUEST, validate_errors=1)


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = BusinessCard.objects.all()
    serializer_class = BusinessCardWithIdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    vacation_data = ''

    def list(self, request):
        user_id = request.user.id
        published = self.request.query_params.get('published', None)
        business_id = self.request.query_params.get('business_id', None)
        is_active = self.request.query_params.get('is_active', None)
        vacation_data_check = 0
        # ---------------------- Filter ------------------------ #
        if published is not None and user_id is not None:
            if published == '0':
                self.queryset = self.queryset.select_related(
                    'user_id').filter(user_id=user_id, status=0, is_active=1)
            elif published == '1':
                self.queryset = self.queryset.select_related(
                    'user_id').filter(user_id=user_id, status=1, is_active=1)

        elif is_active is not None and user_id is not None:
            self.queryset = self.queryset.select_related(
                'user_id').filter(user_id=user_id, is_active=0, status=0)

        elif user_id is not None and business_id == 'all':
                # ----------------- All user business card ---------- #
            self.queryset = self.queryset.select_related(
                'user_id').filter(user_id=user_id)
            self.vacation_data = VacationCard.objects.all().filter(user_id=user_id)
            vacation_data_check = 1
        elif user_id is not None:
            self.queryset = self.queryset.select_related(
                'user_id').filter(user_id=user_id)

        # ------------------------- End ------------------------- #
        serializer = self.serializer_class(self.queryset, many=True)

        if vacation_data_check:
            data = {}
            data['business_cards'] = serializer.data
            data['vacation_cards'] = ""
            vacation_data = []
            for item in self.vacation_data:
                vacation_data.append(
                    {"id": item.id, "user_id": item.user_id.id})
            data['vacation_cards'] = vacation_data
            return CustomeResponse(data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)

    # --------------Method: GET retrieve single record--------------- #
    def retrieve(
            self,
            request,
            pk=None,
            contact_id_new=None,
            call_from_function=None):
        queryset = self.queryset
        user_id = request.user.id
        bcard_obj = get_object_or_404(BusinessCard, pk=pk, user_id=user_id)
        serializer = self.serializer_class(
            bcard_obj, context={'request': request})
        media = ContactMedia.objects.filter(
            contact_id=contact_id_new, front_back__in=[
                1, 2], status=1).values(
            'img_url', 'front_back')
        data = {}
        data = serializer.data
        if media:
            try:
                for item in media:
                    if item['front_back'] == 1:
                        data['bcard_image_frontend'] = str(
                            settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(item['img_url'])
                    elif item['front_back'] == 2:
                        data['bcard_image_backend'] = str(
                            settings.DOMAIN_NAME) + str(settings.MEDIA_URL) + str(item['img_url'])
            except:
                pass

        if call_from_function:
            return data
        else:
            return CustomeResponse(data, status=status.HTTP_200_OK)

    # ------Method: POST create new business card and other operation ------- #
    def create(self, request, call_from_func=None, offline_data=None):

        try:
            user_id = request.user.id
        except:
            user_id = None
    # -------------------- First Validate the json contact data --------------- #
        try:
            validictory.validate(
                request.data["bcard_json_data"], BUSINESS_CARD_DATA_VALIDATION)
        except validictory.ValidationError as error:
            return CustomeResponse(
                {'msg': error.message}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        except validictory.SchemaError as error:
            return CustomeResponse(
                {'msg': error.message}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        except:
            return CustomeResponse(
                {
                    'msg': "Please provide bcard_json_data in json format"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
        # ------------------- End -------------- #

        if call_from_func:
            # -------------- Call from offline app ---------------- #
            tempData = offline_data
        else:
            tempData = request.data.copy()
            tempData["user_id"] = user_id

        serializer = BusinessCardSerializer(
            data=tempData, context={'request': request})

        if serializer.is_valid():
            contact_serializer = ContactsSerializer(
                data=tempData, context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact_serializer.validated_data['businesscard_id'] = business
                contact_serializer = contact_serializer.save()

                bcards = BusinessCard.objects.get(id=business.id)
                contact = bcards.contact_detail
                user = request.user
                # -------------- Save Notes ------------ #
                data_new = serializer.data.copy()

                if "business_notes" in request.data:
                    try:
                        from apps.notes.models import Notes
                        if "note_frontend" in request.data["business_notes"] and request.data[
                                "business_notes"]['note_frontend']:
                            note_frontend_obj = Notes(
                                user_id=user,
                                contact_id=contact,
                                note=request.data["business_notes"]['note_frontend'],
                                bcard_side_no=1)
                            note_frontend_obj.save()
                        if "note_backend" in request.data["business_notes"] and request.data[
                                "business_notes"]['note_backend']:
                            note_frontend_obj = Notes(
                                user_id=user,
                                contact_id=contact,
                                note=request.data["business_notes"]['note_backend'],
                                bcard_side_no=2)
                            note_frontend_obj.save()
                    except:
                        pass
                data_new["business_notes"] = serializer.fetch_notes(bcards)
                # -------------------------End------------ #

                # Assign  first created business card to created default folder
                queryset_folder = Folder.objects.filter(
                    user_id=user_id, foldertype='PR', businesscard_id__isnull=True)
                if not queryset_folder:
                    folder_view = FolderViewSet.as_view({'post': 'create'})
                    offline_data = {}
                    offline_data['businesscard_id'] = business.id
                    offline_data['foldername'] = 'PR Folder'
                    folder_view = folder_view(request, offline_data)
                    data_new["folder_info"] = folder_view.data['data']
                else:
                    queryset_folder.update(businesscard_id=business.id)
                    # data_new["folder_info"]=folder_info
                # -------------------- End ------------------- #
            else:
                return CustomeResponse(
                    contact_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)

            return CustomeResponse(data_new, status=status.HTTP_201_CREATED)

        else:
            return CustomeResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    def update(self, request, pk=None, call_from_func=None, offline_data=None):
        # -------------- First Validate the json contact data ------ #
        try:
            validictory.validate(
                request.data["bcard_json_data"], BUSINESS_CARD_DATA_VALIDATION)
        except validictory.ValidationError as error:
            return CustomeResponse(
                {'msg': error.message}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        except validictory.SchemaError as error:
            return CustomeResponse(
                {'msg': error.message}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        except:
            return CustomeResponse(
                {
                    'msg': "Please provide bcard_json_data in json format"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
        # ---------------------- - End ----------------------------------------------------------- #
        if call_from_func:
            data = offline_data
            pk = offline_data["bcard_id"]
            user_id = offline_data["user_id"]
        else:
            data = request.data.copy()
            user_id = request.user.id
            data['user_id'] = request.user.id
        try:
            bcards = BusinessCard.objects.get(id=pk)
        except:
            if call_from_func:
                return rawResponse('record not found')
            else:
                return CustomeResponse(
                    {'msg': 'record not found'}, status=status.HTTP_404_NOT_FOUND, validate_errors=1)

        serializer = BusinessCardSerializer(
            bcards, data=data, context={'request': request})
        if serializer.is_valid():
            contact = Contacts.objects.get(businesscard_id=pk)
            contact_serializer = ContactsSerializer(
                contact, data=data, context={'request': request})
            if contact_serializer.is_valid():
                business = serializer.save()
                contact_new = contact_serializer.save()
                user = User.objects.get(id=user_id)
                # -------------- Save Notes --------------- #
                data_new = serializer.data.copy()
                # try:
                if "business_notes" in request.data:
                    from apps.notes.models import Notes
                    if "note_frontend" in request.data["business_notes"] and request.data["business_notes"][
                            'note_frontend']:
                        try:
                            note_frontend_obj = Notes.objects.get(
                                user_id=user,
                                contact_id=contact,
                                bcard_side_no=1)
                        except ObjectDoesNotExist:
                            note_frontend_obj = Notes(
                                user_id=user,
                                contact_id=contact,
                                bcard_side_no=1)
                        note_frontend_obj.note = request.data["business_notes"]['note_frontend']
                        note_frontend_obj.save()

                    if "note_backend" in request.data["business_notes"] and request.data["business_notes"][
                            'note_backend']:
                        try:
                            note_frontend_obj = Notes.objects.get(
                                user_id=user,
                                contact_id=contact,
                                bcard_side_no=2)
                        except ObjectDoesNotExist:
                            note_frontend_obj = Notes(
                                user_id=user,
                                contact_id=contact,
                                bcard_side_no=2)
                        note_frontend_obj.note = request.data["business_notes"]['note_backend']
                        note_frontend_obj.save()

                # except:
                #    pass
                data_new["business_notes"] = serializer.fetch_notes(bcards)
            else:
                return CustomeResponse(
                    contact_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)

            return CustomeResponse(data_new, status=status.HTTP_200_OK)

        else:
            return CustomeResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    # ---------------------------- Duplicate the business card --------------- #
    @list_route(methods=['post'],)
    def duplicate(self, request):
        try:
            user_id = request.user.id
        except:
            user_id = None

        try:
            bcard_id = request.data["bcard_id"]
        except:
            bcard_id = None

        if bcard_id and user_id:
            from functions import createDuplicateBusinessCard
            data = createDuplicateBusinessCard(bcard_id, user_id)

            if data:
                data = self.retrieve(
                    request,
                    pk=data['bcards_id_new'],
                    contact_id_new=data['contact_id_new'],
                    call_from_function=1)
            else:
                return CustomeResponse(
                    {
                        "msg": "some problem occured on server side."},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
            return CustomeResponse(data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse({"msg": "Please provide bcard_id and user_id"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    # ----------------------------- End ---------------------- #

    def mergeSkills(self, m, t, u):
        target_bcard = BusinessCardAddSkill.objects.filter(
            businesscard_id__in=m, user_id=u)
        if target_bcard:
            target_bcard.update(businesscard_id=t)
        return target_bcard

    # ---------------------------- Merge business card ------------------------------------- #
    def mergeDict(self, s, f):
        for k, v in f.iteritems():
            if isinstance(v, collections.Mapping):
                r = self.mergeDict(s.get(k, {}), v)
                s[k] = r
            elif isinstance(v, list):
                result = []
                """ TODO : optimization """

                if k == 'basic_info':
                    for valf in v:
                        if 'keyName' in valf:
                            for vals in s.get(k, {}):
                                if valf['keyName'] in vals.values() and vals['value'] != "" and valf[
                                        'value'] == "":
                                    valf['value'] = vals['value']
                            result.append(valf)
                    """ Reverse loop is for check  extra data in second business card """
                    for vals1 in s.get(k, {}):
                        if 'keyName' in vals1:
                            check = 0
                            for valf1 in v:
                                if vals1['keyName'] in valf1.values():
                                    check = 1
                            if not check:
                                result.append(vals1)
                else:
                    v.extend(s.get(k, {}))
                    for myDict in v:
                        if myDict not in result:
                            result.append(myDict)

                s[k] = result
            else:
                # ------------- If the key is blank in first business card then second business card value assign to it ----- #
                if not v and s.get(k, {}):
                    pass
                else:
                    s[k] = f[k]
        return s

    @list_route(methods=['post'],)
    def merge(self, request):
        try:
            user_id = request.user.id
        except:
            user_id = None
        try:
            merge_bcards_ids = request.data["merge_bcards_ids"]
            target_bcard_id = request.data["target_bcard_id"]
        except:
            merge_bcards_ids = None
            target_bcard_id = None

        # Get the  target_bcard_id and merge_bcards_ids data
        if merge_bcards_ids and target_bcard_id and user_id:
            target_bacard = BusinessCard.objects.select_related().get(
                id=target_bcard_id, user_id=user_id)
            first_json = json.loads(json.dumps(
                target_bacard.contact_detail.bcard_json_data))
            # make sure target_bcard_id not in merge_bcards_ids
            if target_bcard_id not in merge_bcards_ids:
                merge_bcards = BusinessCard.objects.filter(
                    id__in=merge_bcards_ids, user_id=user_id).all()

                for temp in merge_bcards:
                    contact_json_data = temp.contact_detail.bcard_json_data
                    if contact_json_data:
                        try:
                            second_json = json.loads(
                                json.dumps(contact_json_data))
                        except:
                            second_json = {}
                        third_json = second_json.copy()

                        self.mergeDict(third_json, first_json)

                        # assign the new json
                        target_bacard.contact_detail.bcard_json_data = third_json
                        target_bacard.contact_detail.save(force_update=True)
                        first_json = third_json
                #  TODO Delete the  merge_bcards_ids
                if merge_bcards:
                    self.mergeSkills(merge_bcards_ids,
                                     target_bcard_id, user_id)
                    merge_bcards.delete()
                else:
                    return CustomeResponse(
                        {
                            "msg": "merge_bcards_ids does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)
                # ----------------------- End --------------------------------------------- #

                self.queryset = self.queryset.select_related(
                    'user_id').filter(user_id=user_id, id=target_bcard_id)
                serializer = self.serializer_class(self.queryset, many=True)
                data = {}
                data['business_cards'] = serializer.data
                return CustomeResponse(data, status=status.HTTP_200_OK)

            else:
                return CustomeResponse(
                    {
                        "msg": "Please provide correct target_bcard_id"},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
        else:
            return CustomeResponse(
                {
                    "msg": "Please provide merge_bcards_ids, target_bcard_id"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
    # ----------------------------- End ---------------------------------------------------- #

    #  Delete business card
    @list_route(methods=['post'],)
    def delete(self, request):

        try:
            user_id = request.user.id
        except:
            user_id = None
        try:
            bcard_ids = request.data["bcard_ids"]
        except:
            bcard_ids = None

        if bcard_ids and user_id:
            try:
                business_card = BusinessCard.objects.filter(
                    id__in=bcard_ids, user_id=user_id)
                if business_card:
                    business_card.delete()
                    return CustomeResponse(
                        {"msg": "business card deleted successfully."}, status=status.HTTP_200_OK)
                else:
                    return CustomeResponse(
                        {
                            "msg": "business card does not exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)
            except:
                return CustomeResponse(
                    {
                        "msg": "some problem occured on server side during delete business cards"},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)

    # ----------------------------- End ---------------- #

    # Inactive Business Card
    @list_route(methods=['post'],)
    def inactive(self, request):

        try:
            user_id = request.user.id
        except:
            user_id = None
        try:
            bcards_id = request.data["bcards_ids"]
        except:
            bcards_id = None
        if bcards_id:
            try:
                BusinessCard.objects.filter(
                    id__in=bcards_id, user_id=user_id).update(
                    is_active=0, status=0)
                return CustomeResponse(
                    {"msg": "Business cards has been inactive"}, status=status.HTTP_200_OK)
            except:
                return CustomeResponse(
                    {
                        "msg": "some problem occured on server side during inactive business cards"},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
        else:
            return CustomeResponse(
                {
                    "msg": "please provide bcards_ids for inactive businesscard"},
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)

    # ------------------------------- End -------------------- #

    # Reactive Business Card
    @list_route(methods=['post'],)
    def reactive(self, request):

        try:
            user_id = request.user.id
        except:
            user_id = None
        try:
            bcard_id = request.data['bcard_id']
        except:
            bcard_id = None
        if bcard_id:
            try:
                bcard_identifier = BusinessCardIdentifier.objects.filter(
                    businesscard_id=bcard_id, status=1)

                if bcard_identifier:
                    businesscardcard_data = BusinessCard.objects.filter(
                        id=bcard_id).update(status=1, is_active=1)

                    if businesscardcard_data:
                        return CustomeResponse(
                            {"msg": "Card has been Reactive successfully"}, status=status.HTTP_200_OK)
                    else:
                        return CustomeResponse(
                            {"msg": "Card not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

                else:
                    return CustomeResponse(
                        {
                            "msg": "Card can't be Reactive as your Business card is not attached with any identifiers  "},
                        status=status.HTTP_400_BAD_REQUEST,
                        validate_errors=1)

            except:
                return CustomeResponse(
                    {
                        "msg": "some problem occured during server side during Reactive business card "},
                    status=status.HTTP_400_BAD_REQUEST,
                    validate_errors=1)
        else:
            return CustomeResponse({"msg": "Business Card not found"},
                                   status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    def destroy(self, request, pk=None):
        return CustomeResponse({'msg': 'record not found'},
                               status=status.HTTP_404_NOT_FOUND, validate_errors=1)

# create businessCard,folder and connections for grey contacts


class WhiteCardViewSet(viewsets.ModelViewSet):

    def create(self, request, from_white_contact=None, cid=None, sid=None):

        try:
            user_id = from_white_contact
            sender_user_id = sid
        except:
            user_id = None
        tempData = {}
        tempData["user_id"] = user_id

        serializer = BusinessCardSerializer(
            data=tempData, context={'request': request})

        if serializer.is_valid():
            business = serializer.save()
            # Assign  first created business card to created default folder
            queryset_folder = Folder.objects.filter(
                user_id=user_id, foldertype='PR').values()
            sender_user_data = BusinessCard.objects.filter(
                user_id=sender_user_id).values()

            if not queryset_folder:
                user = business.user_id
                user_id = user.id
                offline_data = {}
                offline_data['businesscard_id'] = business.id
                offline_data['user_id'] = user_id
                offline_data['foldername'] = 'PR'
                serializer = FolderSerializer(
                    data=offline_data, context={'request': request})

                if serializer.is_valid():
                    receiver_folder = serializer.save(user_id=user)
                    # data from signup form from web
                    Contacts.objects.filter(
                        id=cid).update(
                        businesscard_id=offline_data['businesscard_id'],
                        user_id=from_white_contact)
                    receiver_folder_id = Folder.objects.get(
                        id=receiver_folder.id)
                    receiver_contact_id = Contacts.objects.get(id=cid)
                    sender_data = FolderContact.objects.filter(
                        user_id=sid, contact_id=cid)
                    sender_folder_id = Folder.objects.get(
                        id=sender_data[0].folder_id.id)
                    sender_businesscard_id = sender_folder_id.businesscard_id
                    sender_contact_id = Contacts.objects.get(
                        businesscard_id=sender_businesscard_id)

                    # create connections - folderContact
                    contact_share = SendAcceptRequest()
                    contact_share.exchange_business_cards(
                        sender_folder=sender_folder_id,
                        sender_contact_id=sender_contact_id,
                        receiver_contact_id=receiver_contact_id,
                        receiver_folder=receiver_folder_id,
                        sender_user_id=sender_user_id,
                        receiver_user_id=user_id)

        #  ------------------- End ---------------- #

            return CustomeResponse(
                offline_data, status=status.HTTP_201_CREATED)

        else:
            return CustomeResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
                validate_errors=1)
