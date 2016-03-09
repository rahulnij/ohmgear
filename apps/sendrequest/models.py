from django.db import models

# Create your models here.

class Notification(models.Model):  
    
    class Meta:
     db_table = 'ohmgear_invite_white_contacts'
    type = models.CharField(max_length=50,blank=True,null=True)
    senders_id = models.PositiveIntegerField(default=0, blank=True)
    object_pk_url = models.CharField(max_length=100,blank=True,null=True)
    receivers_id = models.PositiveIntegerField(default=0, blank=True)
    message = models.CharField(max_length=200,blank=True,null=True)
    read_status = models.BooleanField(default=False)