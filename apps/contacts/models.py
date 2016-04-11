# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Application imports
from apps.businesscards.models import BusinessCard, BusinessCardTemplate
from simple_history.models import HistoricalRecords
from apps.folders.models import FolderContact


class Contacts(models.Model):

    class Meta:
        db_table = 'ohmgear_contacts_contact'

    businesscard_id = models.OneToOneField(
        BusinessCard,
        null=True,
        blank=True,
        related_name='contact_detail',
        db_column="businesscard_id")
    bcard_json_data = JSONField(null=True)
#    template_id = models.ForeignKey(BusinessCardTemplate,db_column="template_id")
    user_id = models.ForeignKey(User, db_column="user_id")
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return '{"id":"%s","bcard_json_data":"%s","businesscard_id":"%s"}' % (
            self.id, self.bcard_json_data, self.businesscard_id)


class ContactMedia(models.Model):

    class Meta:
        db_table = 'ohmgear_contact_media'
    user_id = models.ForeignKey(User, db_column="user_id")
    contact_id = models.ForeignKey(
        "Contacts", db_column='contact_id', related_name='businesscard_media')
    img_url = models.ImageField(
        _("Image Url"), upload_to='uploads/bcards_gallary/', max_length=254)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
    front_back = models.IntegerField(
        _("Front Back"), default=1)  # 1=Front ,2=Back
    position = models.IntegerField(
        _("Position"), default=1)  # 1=Horizontal ,2=Vertical
    status = models.IntegerField(_("Status"), default=0)

    def __unicode__(self):
        return '{"id:"%s","contact_id":"%s","user_id":"%s","status":"%s","front_back":"%s","img_url":"%s"}' % (
            self.id, self.contact_id, self.user_id, self.status, self.front_back, self.img_url)

from apps.folders.models import FolderContact
class FavoriteContact(models.Model):

    class Meta:
        db_table = 'ohmgear_contacts_favorite_contact'
        unique_together = ('foldercontact_id', 'user_id')
    foldercontact_id = models.ForeignKey(
        FolderContact, db_column='foldercontact_id')
    user_id = models.ForeignKey(User, db_column="user_id")
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id:"%s","foldercontact_id":"%s"}' % (
            self.id, self.foldercontact_id)
# Create Groups to store contacts


class AssociateContact(models.Model):

    class Meta:
        db_table = 'ohmgear_contacts_associate_contact'
        unique_together = (
            'user_id', 'associatefoldercontact_id', 'foldercontact_id')
    user_id = models.ForeignKey(User, db_column='user_id')
    associatefoldercontact_id = models.ForeignKey(
        FolderContact, db_column='associatefoldercontact_id')
    foldercontact_id = models.ForeignKey(
        FolderContact,
        db_column='foldercontact_id',
        related_name='folder_data')
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id:"%s","user_id":"%s","associatefoldercontact_id":"%s","foldercontact_id":"%s"}' % (
            self.id, self.user_id, self.associatefoldercontact_id, self.foldercontact_id)
