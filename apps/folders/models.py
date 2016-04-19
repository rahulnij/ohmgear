
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.businesscards.models import BusinessCard
from apps.contacts.models import Contacts
from datetime import datetime
from django.conf import settings
User = settings.AUTH_USER_MODEL


class FolderType(models.Model):

    class Meta:
        db_table = 'ohmgear_folders_foldertype'


class Folder(models.Model):

    class Meta:
        db_table = 'ohmgear_folders_folder'

    folderType = (
        ('PR', "Private"),
    )
    foldername = models.CharField(_('folder name'), max_length=30, null=False, blank=False, error_messages={
                                  'blank': 'Folder name can not be empty.'})
    foldertype = models.CharField(
        _('folder type'), max_length=2, null=False, blank=False, choices=folderType, default='PR')
    status = models.IntegerField(_('status'), default=1)
    user_id = models.ForeignKey(User, verbose_name=_(
        'user'), null=False, db_column='user_id')
    businesscard_id = models.ForeignKey(BusinessCard, verbose_name=_(
        'business card'), null=True, blank=True, db_column='businesscard_id')
    created_date = models.DateTimeField(
        _('created date'), default=datetime.utcnow, blank=True)
    updated_date = models.DateTimeField(
        _('updated date'), default=datetime.utcnow, blank=True)

    def __unicode__(self):
        return '{"id":%d,"foldername":%s,"foldertype":%s ,"businesscard_id":%s}' % \
            (self.id, self.foldername, self.foldertype, self.businesscard_id)


class FolderContact(models.Model):

    class Meta:
        db_table = 'ohmgear_folders_folder_contact'
        unique_together = ('folder_id', 'contact_id')

    linkStatus = (
        (0, "White"),
        (1, "Orange"),
        (2, "Green"),
        (3, "Blue"),
    )

    user_id = models.ForeignKey(User, null=False, db_column='user_id')

    folder_id = models.ForeignKey(Folder, db_column='folder_id')
    contact_id = models.ForeignKey(
        Contacts, db_column='contact_id', related_name='folder_contact_data')

    link_status = models.IntegerField(
        _('link_status'), default=0, choices=linkStatus)
    is_linked = models.IntegerField(_('status'), default=0)

    created_date = models.DateTimeField(
        _('created date'), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _('updated date'), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":%d,"folder_id":%d,"contact_id":%d,"link_status":%d,"is_linked":%d}' % \
            (self.id, self.folder_id.id, self.contact_id.id, self.link_status, self.is_linked)


class MatchContact(models.Model):

    class Meta:
        db_table = 'ohmgear_folders_match_contacts'
        unique_together = ('folder_contact_id', 'businesscard_id')

    user_id = models.ForeignKey(User, null=False, db_column='user_id')
    folder_contact_id = models.ForeignKey(
        FolderContact, db_column='folder_contact_id')
    businesscard_id = models.ForeignKey(BusinessCard, verbose_name=_(
        'business card'), null=True, blank=True, db_column='businesscard_id')
    created_date = models.DateTimeField(
        _('created date'), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _('updated date'), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":%d,"user_id":%d,"folder_contact_id":%d,"businesscard_id":%d}' % \
            (self.id, self.user_id.id, self.folder_contact_id.id, self.businesscard_id.id)
