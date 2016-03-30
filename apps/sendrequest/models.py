from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Notification(models.Model):  
    
    class Meta:
     db_table = 'ohmgear_send_request'
     
    type = models.CharField(max_length=50,blank=True,null=True)
    sender_id = models.PositiveIntegerField(default=0, blank=True)
    object_pk_url = models.CharField(max_length=400,blank=True,null=True)
    receiver_id = models.PositiveIntegerField(default=0, blank=True)
    message = models.CharField(max_length=200,blank=True,null=True)
    read_status = models.BooleanField(default=0)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateField(_("Updated Date"),auto_now_add=False,auto_now=True)    