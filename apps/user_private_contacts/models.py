from django.db import models
from apps.businesscards.models import BusinessCard
from apps.users.models import User

# Create your models here.
class Contacts(models.Model):
    class Meta:
        db_table = 'ohmgear_contacts_contact_copy'
    businesscard_id_copy = models.OneToOneField(BusinessCard,related_name='contact_detail_copy',db_column="businesscard_id_copy")
    bcard_json_data_copy = JsonField(null=True)
    user_id_copy = models.ForeignKey(User,db_column="user_id")
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return '{"id":"%s","bcard_json_data_copy":"%s","businesscard_id_copy":"%s"}'%(self.id,self.bcard_json_data_copy,self.businesscard_id_copy)