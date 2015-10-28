from django.db import models
from apps.contacts.models import Contacts
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class Promocode(models.Model):
    class Meta:
        db_table = 'ohmgear_promocodes'
    promocode_title = models.CharField(_('Promocode Title'),max_length=50,null=True, unique=True)
    promocode_worth  =        models.CharField(_('Promocode Worth'),max_length=500,null=True)
    created_date  = models.DateTimeField(_('Created Date'),auto_now_add = True)
    expiry_date =      models.DateTimeField(_('Expiry Date'),max_length=50,null=True)
    user_type =       models.IntegerField(_('User Type'),null=True)
    no_of_use =          models.IntegerField(_('Maximum Usage'),null=True)
      
    
    
    
    
    
    
