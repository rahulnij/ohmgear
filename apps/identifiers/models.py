from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.db.models.User import User
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

TEMPLATE_TYPE = (('1', 'option1'),
                  ('2', 'option2'),
                  ('3', 'option3'),                  
                 )
      
IDENTIFIER_TYPE = (('1','System Generated'),
                    ('2','Premium'),
                    )
class Identifier(models.Model):
    
    class Meta:
     db_table = 'ohmgear_identifiers_identifier'
    
    user = models.ForeignKey(User)
    identifier = models.CharField(_("identifier"),max_length=12,unique=True)
    #-------------Identifier status whether identifier is active or not or is expired for business card---# 
    status      = models.IntegerField(_("Status"),default=1)
    #--------------Payment status whether user have paid for idnetifier or not
    paymentstatus      = models.IntegerField(_("Payment Status"),default=0)
    #---------------- identifier type 1 for system generated and 2 for premium----#
    identifier_type = models.IntegerField(_("Identifier Type"))
    #---------------- identifier last date which date identifier will get expired----#
    idetifierlastdate  = models.DateTimeField(_("Identifier Last Date"))
    created_date = models.DateTimeField(_("Created Date"),auto_now_add=True)
    updated_date = models.DateTimeField(_("Updated Date"),auto_now_add= True)
    
    
    def __unicode__(self):
        return'{"id:"%s","identifier_type":"%s"}'%(self.id,self.identifier_type)
