from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from apps.folders.models import FolderContact
User = settings.AUTH_USER_MODEL


# Create your models here.

class Group(models.Model):

    class Meta:
        db_table = 'ohmgear_groups_group'
    group_name = models.CharField(_("Group Name"), max_length=60)
    user_id = models.ForeignKey(User, db_column="user_id")
    status = models.IntegerField(_('status'), default=1)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.TimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","group_name":"%s","user_id":"%s"}' % (self.id, self.group_name, self.user_id)


class GroupContacts(models.Model):

    class Meta:
        db_table = 'ohmgear_groups_group_contact'
        unique_together = ('group_id', 'folder_contact_id',)
    folder_contact_id = models.ForeignKey(
        FolderContact, db_column='folder_contact_id')
    group_id = models.ForeignKey(
        Group, db_column='group_id', related_name='group_data')
    user_id = models.ForeignKey(User, db_column="user_id")
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.TimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","group_id":"%s","user_id":"%s"}' % (self.id, self.group_id, self.user_id)
