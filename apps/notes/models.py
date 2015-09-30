from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class Notes(models.Model):
    class Meta:
        db_table = 'ohmgear_notes'
    note_headline = models.CharField(_('Note Headline'),max_length=50,null=True)
    note  =        models.CharField(_('Notes'),max_length=50,null=True)
    created_date  = models.DateTimeField(_('Created Date'),auto_now_add = True)
    location =      models.CharField(_('location'),max_length=50,null=True)
    user =          models.OneToOneField(User,null=True)
    updated_date  = models.DateTimeField(_('Updated Date'),auto_now_add = True)
    
    
    def __unicode__(self):
        return '{"id":"%s","note_headline":"%s","note":"%s","created_date":"%s","location":"%s","user":"%s"}' %(self.id,self.note_headline,self.note,self.created_date,self.location,self.user)
    
    
    
    
    
