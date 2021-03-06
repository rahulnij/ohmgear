# Return token if does not exit then create
from models import BusinessCard
from apps.contacts.models import Contacts, ContactMedia
from apps.notes.models import Notes


def createDuplicateBusinessCard(bcard_id=None, user_id=None):

    if bcard_id and user_id:
        # Duplicate Business card row
        try:
            bcards = BusinessCard.objects.select_related(
                "contact_detail").get(id=bcard_id, user_id=user_id)
        except:
            return None
        bcards.id = None
        bcards.status = 0
        if bcards.name:
            bcards.name = "copy %s" % (bcards.name)
        bcards.save()
        bcards_id_new = bcards.id
        contact_id = bcards.contact_detail.id
        # End

        # Duplicate Contact row
        try:
            contact = Contacts.objects.get(businesscard_id=bcard_id)
            contact.id = None
            contact.businesscard_id = BusinessCard.objects.get(
                id=bcards_id_new)
            contact.save()
            contact_id_new = contact.id
        except:
            pass
        # End
        # Duplicate Notes
        try:
            note = Notes.objects.get(contact_id=contact_id, bcard_side_no=1)
            note.contact_id = Contacts.objects.get(id=contact_id_new)
            note.id = None
            note.save()
        except:
            pass

        try:
            note = Notes.objects.get(contact_id=contact_id, bcard_side_no=2)
            note.contact_id = Contacts.objects.get(id=contact_id_new)
            note.id = None
            note.save()
        except:
            pass

        try:
            bcard_image = ContactMedia.objects.get(
                contact_id=contact_id, user_id=user_id, front_back=1, status=1)
            bcard_image.contact_id = Contacts.objects.get(id=contact_id_new)
            bcard_image.id = None
            bcard_image.save()
        except:
            pass

        try:
            bcard_image = ContactMedia.objects.get(
                contact_id=contact_id, user_id=user_id, front_back=2, status=1)
            bcard_image.contact_id = Contacts.objects.get(id=contact_id_new)
            bcard_image.front_back = 2
            bcard_image.id = None
            bcard_image.save()
        except:
            pass
        data = {}
        data['bcards_id_new'] = bcards_id_new
        data['contact_id_new'] = contact_id_new
        return data
        # End

        # Return the new business card

        # End


class DiffJson(object):

    def __init__(self, first, second, with_values=False, vice_versa=False):
        self.difference = []
        self.check(first, second, with_values=with_values)

        if vice_versa:
            self.check(second, first, with_values=with_values)

    def check(self, first, second, path='', with_values=False):
        if second is not None:
            if not isinstance(first, type(second)):
                message = '%s- %s, %s' % (path, type(first), type(second))
                self.save_diff(message, TYPE)

        if isinstance(first, dict):
            for key in first:
                # the first part of path must not have trailing dot.
                if len(path) == 0:
                    new_path = key
                else:
                    new_path = "%s.%s" % (path, key)

                if isinstance(second, dict):
                    if key in second:
                        sec = second[key]
                    else:
                        # there are key in the first, that is not presented in
                        # the second
                        self.save_diff(new_path, PATH)

                        # prevent further values checking.
                        sec = None

                    # recursive call
                    self.check(first[key], sec, path=new_path,
                               with_values=with_values)
                else:
                    # second is not dict. every key from first goes to the
                    # difference
                    self.save_diff(new_path, PATH)
                    self.check(first[key], second,
                               path=new_path, with_values=with_values)

        # if object is list, loop over it and check.
        elif isinstance(first, list):
            for (index, item) in enumerate(first):
                new_path = "%s[%s]" % (path, index)
                # try to get the same index from second
                sec = None
                if second is not None:
                    try:
                        sec = second[index]
                    except (IndexError, KeyError):
                        # goes to difference
                        self.save_diff(
                            '%s - %s, %s' %
                            (new_path, type(first), type(second)), TYPE)

                # recursive call
                self.check(first[index], sec, path=new_path,
                           with_values=with_values)

        # not list, not dict. check for equality (only if with_values is True)
        # and return.
        else:
            if with_values and second is not None:
                if first != second:
                    self.save_diff('%s - %s | %s' %
                                   (path, first, second), VALUE)
            return

    def save_diff(self, diff_message, type_):
        message = '%s: %s' % (type_, diff_message)
        if diff_message not in self.difference:
            self.difference.append(message)


def searchjson(name, value, user_id=None, bcard_id=None):
    """
    search using email and firstname_lastname
    search will return BusinessCard.
    """

    bcards = ''
    contact = ''

    if bcard_id is None:
        bcard_id = []
    else:
        bcard_id = [bcard_id]

    # Search by name.#
    if name == 'firstname_lastname':
        firstName, lastName = value.partition(" ")[0:3:2]
        bcard = BusinessCard.objects.filter(
            status=1,
            contact_detail__bcard_json_data__contains={
                'side_first': {
                    'basic_info': [
                        {
                            'keyName': "FirstName",
                            "value": firstName}]}} or {
                'side_second': {
                    'basic_info': [
                        {
                            'keyName': "FirstName",
                            "value": firstName}]}}).exclude(
            id__in=bcard_id)
        if lastName:

            bcard = bcard.filter(
                contact_detail__bcard_json_data__contains={
                    'side_first': {
                        'basic_info': [
                            {
                                'keyName': "FirstName", "value": firstName}, {
                                'keyName': "LastName", "value": lastName}]}} or
                            {
                    'side_second': {
                        'basic_info': [
                            {
                                'keyName': "FirstName", "value": firstName}, {
                                'keyName': "LastName", "value": lastName}]}})
        return bcard

    # Search by email.#
    if user_id and name == "email":

        bcard_sql = 'SELECT * FROM ohmgear_businesscards_businesscard  \
            INNER JOIN ohmgear_contacts_contact ON \
            (ohmgear_businesscards_businesscard.id = \
            ohmgear_contacts_contact.businesscard_id) \
            where ohmgear_businesscards_businesscard.status = 1\
            AND ohmgear_businesscards_businesscard.user_id=%s\
            AND ohmgear_contacts_contact.bcard_json_data @>\
            \'{"side_first": {"contact_info": {"email": [{"data": "%s"}]}}}\'\
            order by ((ohmgear_contacts_contact.bcard_json_data  #>> \
            \'{side_first,basic_info}\')::jsonb->>1) ASC, \
            ((ohmgear_contacts_contact.bcard_json_data  #>> \
            \'{side_first,basic_info}\')::jsonb->>2) ASC ,\
            ((ohmgear_contacts_contact.bcard_json_data  #>> \
            \'{side_second,basic_info}\')::jsonb->>1) ASC ,\
            ((ohmgear_contacts_contact.bcard_json_data  #>> \
            \'{side_second,basic_info}\')::jsonb->>2) ASC ' % (user_id, value)

        bcards = BusinessCard.objects.raw(bcard_sql)

    if bcards:
        bcards_id = []

        for data in bcards:
            bcards_id.append(data.id)
        bcards_id = ', '.join(map(str, bcards_id))

    else:
        bcards_id = '0'

    contact_sql = 'SELECT * FROM ohmgear_businesscards_businesscard  \
        INNER JOIN ohmgear_contacts_contact ON \
        (ohmgear_businesscards_businesscard.id = \
        ohmgear_contacts_contact.businesscard_id)\
        where ohmgear_businesscards_businesscard.status = 1 AND NOT \
        ohmgear_businesscards_businesscard.id IN (%s) \
        AND ohmgear_contacts_contact.bcard_json_data @>\
        \'{"side_first": {"contact_info": {"email": [{"data": "%s"}]}}}\'\
        order by ((ohmgear_contacts_contact.bcard_json_data  #>> \
        \'{side_first,basic_info}\')::jsonb->>1) ASC, \
        ((ohmgear_contacts_contact.bcard_json_data  #>> \
        \'{side_first,basic_info}\')::jsonb->>2) ASC ,\
        ((ohmgear_contacts_contact.bcard_json_data  #>> \
        \'{side_second,basic_info}\')::jsonb->>1) ASC ,\
        ((ohmgear_contacts_contact.bcard_json_data  #>> \
        \'{side_second,basic_info}\')::jsonb->>2) ASC ' % (bcards_id, value)

    contact = BusinessCard.objects.raw(contact_sql)

    if bcards or contact:
        result_list = []
        from itertools import chain
        result_list = list(chain(bcards, contact))
        return result_list
    else:
        return False
