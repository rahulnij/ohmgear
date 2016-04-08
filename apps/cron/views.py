# Import Python Modules
import datetime
import json

# Third Party Imports
from django.shortcuts import render
import rest_framework.status as status
from rest_framework.decorators import api_view
from rest_framework import viewsets

# Local app imports
from apps.identifiers.models import Identifier
from functions import CreateSystemIdentifier
from ohmgear.functions import CustomeResponse
from apps.contacts.models import Contacts
from apps.contacts.serializer import ContactsSerializer
from apps.contacts.views import storeContactsViewSet
from apps.folders.models import FolderContact, MatchContact
from apps.folders.serializer import MatchContactSerializer


@api_view(['GET', 'POST'])
def updateidentifierstatus(request, **kwargs):

    if request.method == 'GET':

        currentdate = datetime.date.today()
        """ First time user will get premium identifier for 3 months after that
         premium identifier will replace by sytem identifier"""
        getfreeexpiredpremiumidentifier = Identifier.objects.filter(
            identifierlastdate=currentdate,
            paymentstatus=0,
            status=1,
            identifiertype=2,
            totalmonths=3).values()
        if getfreeexpiredpremiumidentifier:
            # premium identifier replaced by system
            totalrecord = getfreeexpiredpremiumidentifier.count()

            for i in range(totalrecord):
                Identifier.objects.filter(
                    id=getfreeexpiredpremiumidentifier[i]['id']).update(
                    identifier=CreateSystemIdentifier(),
                    identifiertype=1,
                    identifierlastdate=str(
                        (datetime.date.today() +
                         datetime.timedelta(
                            3 *
                            365 /
                            12)).isoformat()))
                # print "run api for systematic identifier"

        # After 3 months of premium identifier system identifier will be given
        # for  3 months  and after that it will get expire and identifier
        # status will be 0-------#
        getfreeexpiredsystemidentifier = Identifier.objects.filter(
            identifierlastdate=currentdate,
            paymentstatus=0,
            status=1,
            identifiertype=1).values()
        if getfreeexpiredsystemidentifier:
            totalfreeexpiredsystemidentifierrecord = getfreeexpiredsystemidentifier.count()

            for i in range(totalfreeexpiredsystemidentifierrecord):
                Identifier.objects.filter(id=getfreeexpiredsystemidentifier[
                                          i]['id']).update(status=0)

            # print "update query make status 0 "

        # premium identifier user have paid for premium but now expired
        # -------#
        getpaidexpiredpremiumidentifier = Identifier.objects.filter(
            identifierlastdate=currentdate,
            paymentstatus=1,
            status=1,
            identifiertype=2).values()
        if getpaidexpiredpremiumidentifier:
            totalpaidexpiredpremiumidentifierrecord = getpaidexpiredpremiumidentifier.count()

            for i in range(totalpaidexpiredpremiumidentifierrecord):
                Identifier.objects.filter(
                    id=getpaidexpiredpremiumidentifier[i]['id']).update(
                    status=0, paymentstatus=0)
                # print "update query make status 0 and payement status 0 for
                # premium identifier"

        # System identifier user have paid for system but now expired  -------#
        getpaidexpiredsystemidentifier = Identifier.objects.filter(
            identifierlastdate=currentdate,
            paymentstatus=1,
            status=1,
            identifiertype=1).values()
        if getpaidexpiredsystemidentifier:
            totalpaidexpiredsystemidentifier = getpaidexpiredsystemidentifier.count()

            for i in range(totalpaidexpiredsystemidentifier):
                Identifier.objects.filter(
                    id=getpaidexpiredsystemidentifier[i]['id']).update(
                    status=0, paymentstatus=0)
        # print "update query make status 0 and payement status 0 for system
        # identifier"

        return CustomeResponse(
            {'msg': "Cron runnig successfully"}, status=status.HTTP_200_OK)


class UpdateContactLinkStatusCron(viewsets.ModelViewSet):

    # No need to authentication as it will run as a cron
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    http_method_names = ['get']

    def list(self, request):
        # Fetch the all users contact
        queryset_contact_without_bcard = self.queryset.filter(
            businesscard_id__isnull=True).order_by("user_id")
        queryset_contact_have_bcard = self.queryset.filter(
            businesscard_id__isnull=False).order_by("user_id")
        queryset_serializer = ContactsSerializer(
            queryset_contact_have_bcard, many=True)

        if queryset_serializer.data is not None:
            contacts_copy = queryset_serializer.data
            match_contact_insert = []
            store_object = storeContactsViewSet()
            for value in queryset_contact_without_bcard:

                iterator = iter(contacts_copy)
                try:
                    while True:
                        value_copy = iterator.next()
                        if value.user_id.id != value_copy["user_id"]:

                            if value.bcard_json_data and value_copy[
                                    "bcard_json_data"]:
                                # print value.user_id.id,value_copy["user_id"]
                                result = store_object.find_duplicate(
                                    value.bcard_json_data, json.loads(
                                        value_copy["bcard_json_data"]))
                                # print result
                            else:
                                result = ''
                            # print result
                            if result:
                                # Change the link status then insert into MatchContact Model
                                # related field is not working
                                # value.folder_contact
                                try:
                                    folder_contact = FolderContact.objects.get(
                                        contact_id=value.id, user_id=value.user_id)
                                    if folder_contact.link_status == 0:
                                        folder_contact.link_status = 1
                                        folder_contact.save()
                                        match_contact_insert.append(
                                            {
                                                "user_id": value.user_id.id,
                                                "folder_contact_id": folder_contact.id,
                                                "businesscard_id": value_copy['businesscard_id']})
                                except:
                                    pass
                                # match_contact_insert = MatchContactSerializer({''})
                            # pass
                except StopIteration:
                    pass

            if match_contact_insert:
                #                      match_contact_insert = MatchContactSerializer(data=match_contact_insert,many=True)
                #                      if match_contact_insert.is_valid():
                #                         match_contact_insert.save()
                #                      else:
                # return
                # CustomeResponse(match_contact_insert.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                for items in match_contact_insert:
                    match_contact_serializer = MatchContactSerializer(
                        data=items)
                    if match_contact_serializer.is_valid():
                        match_contact_serializer.save()
                    else:
                        pass
        # Note : TODO we will change the order of execution  of find_duplicate
        return CustomeResponse(
            {"msg": "run successfully"}, status=status.HTTP_200_OK)
