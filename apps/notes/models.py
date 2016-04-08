from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from apps.contacts.models import Contacts
User = settings.AUTH_USER_MODEL


class Notes(models.Model):

    class Meta:
        db_table = 'ohmgear_notes'
        unique_together = ('contact_id', 'user_id', 'bcard_side_no')
    note_headline = models.CharField(
        _('Note Headline'), max_length=50, null=True)
    note = models.CharField(_('Notes'), max_length=500, null=True)
    location_area = models.CharField(
        _('Location Area'), max_length=50, null=True)
    contact_id = models.ForeignKey(Contacts, db_column="contact_id")
    user_id = models.ForeignKey(User, db_column="user_id")
    # single side is 1 double side is 2
    bcard_side_no = models.IntegerField(_('BCARD SIDE NO'), default=1)
    # Note Accesibility by default 0 for public 1 for shared
    note_accessibilty = models.IntegerField(_('Note Accessbility'), default=0)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","note_headline":"%s","note":"%s","location_area":"%s","note_accessibilty":"%s","contact_id":"%s","user_id":"%s","bcard_side_no":"%s"}' % (
            self.id, self.note_headline, self.note, self.location_area, self.note_accessibilty, self.contact_id, self.user_id, self.bcard_side_no)
