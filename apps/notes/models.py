from django.db import models
from apps.contacts.models import Contact
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class Notes(models.Model):
    class Meta:
        db_table = 'ohmgear_notes'
        unique_together = ('contact', 'user','bcard_side_no')
    note_headline = models.CharField(_('Note Headline'),max_length=50,null=True)
    note  =        models.CharField(_('Notes'),max_length=500,null=True)
    location_area =      models.CharField(_('Location Area'),max_length=50,null=True)
    contact =       models.ForeignKey(Contact)
    user =          models.ForeignKey(User)
    #------------ single side is 1 double side is 2----#
    bcard_side_no = models.IntegerField(_('BCARD SIDE NO'),default =1)
    #------------------ Note Accesibility by default 0 for public 1 for shared  -------------------#  
    note_accessibilty  = models.IntegerField(_('Note Accessbility'),default =0)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return '{"id":"%s","note_headline":"%s","note":"%s","location_area":"%s","note_accessibilty":"%s","contact":"%s","user":"%s","bcard_side_no"}' %(self.id,self.note_headline,self.note,self.location_area,self.note_accessibilty,self.contact,self.user,self.bcard_side_no)
    
    
    
    
    
