from django.db import models
from apps.businesscards.models import BusinessCard,BusinessCardTemplate
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_pgjson.fields import JsonField
from django.conf import settings
from simple_history.models import HistoricalRecords
User = settings.AUTH_USER_MODEL


# Create your models here.

class Contacts(models.Model):
    class Meta:
        db_table = 'ohmgear_contacts_contact'
    businesscard_id = models.OneToOneField(BusinessCard,null=True, blank=True,related_name='contact_detail',db_column="businesscard_id")
    bcard_json_data = JsonField(null=True)
#    template_id = models.ForeignKey(BusinessCardTemplate,db_column="template_id")
    user_id = models.ForeignKey(User,db_column="user_id")
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateField(_("Updated Date"),auto_now_add=False,auto_now=True)
    history = HistoricalRecords()
    
    def __unicode__(self):
        return '{"id:"%s","bcard_json_data":"%s","businesscard_id":"%s"}'%(self.id,self.bcard_json_data,self.businesscard_id)
    
    
    
class FavoriteContact(models.Model):
    class Meta:
        db_table = 'ohmgear_contacts_favorite_contact'
        unique_together = ('contact_id', 'user_id')
    contact_id   =  models.ForeignKey(Contacts,db_column='contact_id')
    user_id = models.ForeignKey(User,db_column="user_id")
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return '{"id:"%s","contact_id":"%s"}'%(self.id,self.contact_id)
# Create Groups to store contacts
      

      
      
