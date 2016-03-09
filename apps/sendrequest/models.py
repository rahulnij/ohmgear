from django.db import models

# Create your models here.

class Notification(models.Model):    
    type = models.CharField(max_length=50,blank=True,null=True)
    object_pk = models.PositiveIntegerField(default=0, blank=True)
    object_pk_url = models.CharField(max_length=100,blank=True,null=True)
    action_to = models.ForeignKey(Profile,related_name='notification_action_to')
    message = models.CharField(max_length=200,blank=True,null=True)
    read_status = models.BooleanField(default=False)