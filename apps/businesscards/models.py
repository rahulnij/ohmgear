from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.identifiers.models import Identifier
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class BusinessCardTemplate(models.Model):
    
        class Meta:
            db_table = 'ohmgear_businesscardtemplate'
        template_name = models.CharField(_("Template Name"),max_length=50)
        template_content = models.CharField(_("Template Content"),max_length= 100)
        status  = models.IntegerField(_("Status"),default=0)
        created_date = models.DateTimeField(_('Created Date'))
        updated_date = models.DateTimeField(_('Updated Date'))
        
        def __unicode__(self):
            return '{"id":"%s","template_name":"%s","template_content":"%s"}' %(self.id,self.template_name,self.template_content)
    


class BusinessCard(models.Model):
    
    class Meta:
     db_table = 'ohmgear_businesscard'
    name = models.CharField(_("name"),null=True,max_length=50)
    template = models.OneToOneField('BusinessCardTemplate')
    status = models.IntegerField(_("Status"),default=0)
    is_Actve = models.IntegerField(_("Is Active"),default=1)
    created_date = models.DateTimeField(_("Created Date"),auto_now_add=True)
    updated_date = models.DateTimeField(_("Updated Date"),auto_now_add= True)
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return'{"id:"%s","name":"%s","template_id":"%s"}'%(self.id,self.template_id)
    
    
    

class BusinessCardIdentifier(models.Model):
    
    class Meta:
        db_table = 'ohmgear_businesscardidentifier'
    businesscard = models.OneToOneField('BusinessCard')
    identifier = models.OneToOneField(Identifier)
    created_date    =  models.DateTimeField(_('Created Date'),auto_now_add = True)
    updated_date    =   models.DateTimeField(_('Update Date'),auto_now_add = True)
    
    def __unicode__(self):
        return'{"id:"%s","businesscard":"%s","identifier":"%s"}'%(self.id,self.businesscard,self.identifier)
    
    
    
    