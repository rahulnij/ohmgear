from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from simple_history.models import HistoricalRecords
from django_pgjson.fields import JsonField
User = settings.AUTH_USER_MODEL

#from serializer import BusinessCardMediaSerializer
# Create your models here.

class Feedbacks(models.Model):
    
        class Meta:
            db_table = 'ohmgear_feedback'
        user_id = models.ForeignKey(User,db_column="user_id")
        bug_type = models.CharField(_("Template Content"),max_length=50)
        status  = models.IntegerField(_("Status"),default=0)
        created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
        updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
        
        def __unicode__(self):
            return '{"id":"%s","user_id":"%s","bug_type":"%s"}' %(self.id,self.user_id,self.bug_type)
    