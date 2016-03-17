from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Notification(models.Model):  
    
    class Meta:
     db_table = 'ohmgear_send_request'
    
    AcceptedStatus = (
			(0,"sent"),
                        (1,"accepted"),
                        (2,"not accepted")
		     )
    
    RequestType    = (
                       ("b2b","bcard to bcard"),                       
                     )                 
    type = models.CharField(max_length=50,default="b2b",choices=RequestType)
    sender_id = models.PositiveIntegerField(default=0)
    partial_url = models.CharField(max_length=100,blank=True,null=True)
    receiver_id = models.PositiveIntegerField(default=0, blank=True)
    message = models.CharField(max_length=200,blank=True,null=True)
    read_status = models.BooleanField(default=0)
    accepted_status = models.PositiveIntegerField(default=0, choices=AcceptedStatus)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateField(_("Updated Date"),auto_now_add=False,auto_now=True)    
