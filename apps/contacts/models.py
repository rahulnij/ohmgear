from django.db import models
from apps.businesscards.models import BusinessCard,BusinessCardTemplate
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_pgjson.fields import JsonField
#User = settings.AUTH_USER_MODEL

# Create your models here.

class Contact(models.Model):
    class Meta:
        db_table = 'ohmgear_contacts_contact'
    businesscard = models.OneToOneField(BusinessCard,null=True, blank=True,related_name='contact_detail')
    bcard_json_data = JsonField(null=True)
    template = models.ForeignKey(BusinessCardTemplate)
    created_date= models.DateTimeField(_("Created Date"),auto_now_add = True)
    updated_date= models.DateTimeField(_("Updated Date"),auto_now_add = True)
    def __unicode__(self):
        return '{"id:"%s","bcard_json_data":"%s","businesscard":"%s"}'%(self.id,self.bcard_json_data,self.businesscard)
    
    
        
