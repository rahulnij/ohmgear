from django.db import models
from apps.businesscards.models import BusinessCard
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class contact(models.Model):
    class Meta:
        db_table = 'ohmgear_contacts'
    user = models.OneToOneField(User)
    businesscard = models.OneToOneField(BusinessCard,null=True)
    nickname   =  models.CharField(_("nickname"),null= True,max_length=45)
    company_name = models.CharField(_("Company Name"),max_length = 45)
    title       = models.CharField(_("title"),max_length = 45)
    created_Date= models.DateTimeField(_("Created Date"),auto_now_add = True)
    updated_Date= models.DateTimeField(_("Updated Date"),auto_now_add = True)
    def __unicode__(self):
        return '{"id:"%s","user":"%s","businesscard":"%s","nickname":"%s","company_name":"%s"}'%(self.id,self.user,self.businesscard,self.nickname,self.companyname)
    
    
        
