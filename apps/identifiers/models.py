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
     db_table = 'ohmgear_identifier'
    user = models.OneToOneField(User)
    identifier = models.CharField(_("identifier"),null=True,max_length=50)
    identifier_type = models.IntegerField(_("Identifier Type"),choices=IDENTIFIER_TYPE,default=1)
    created_date = models.DateTimeField(_("Created Date"),auto_now_add=True)
    updated_date = models.DateTimeField(_("Updated Date"),auto_now_add= True)
    
    
    def __unicode__(self):
        return'{"id:"%s","identifier":"%s","identifier_type":"%s"}'%(self.id,self.identifier,self.identifier_type)
