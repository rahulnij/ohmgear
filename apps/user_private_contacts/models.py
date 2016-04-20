from django.db import models
from apps.businesscards.models import BusinessCard
from apps.users.models import User

# It is the the extra information added by user in other users contact--------#
'''
class UserPrivateContactsDetails(models.Model):

    class Meta:
        db_table = 'ohmgear_contacts_contact_copy'
    contact_id = models.OneToOneField(
        BusinessCard, related_name='private_contact_detail', db_column="contact_id")
    # private_json_data = JsonField(null=True)
    user_id = models.ForeignKey(User, db_column="user_id")
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","contact_id":"%s","private_json_data":"%s"}' % (self.id, self.contact_id, self.private_json_data)
'''
