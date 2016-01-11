from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_pgjson.fields import JsonField

# Create your models here.

class About(models.Model):
    
        class Meta:
            db_table = 'ohmgear_about'
        headline = models.CharField(_("Headline"),max_length=50)
        content = models.TextField("Content")
        page_type = models.IntegerField(_("Page Type"),default=1)
        status  = models.IntegerField(_("Status"),default=1)
        created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
        updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
        
        def __unicode__(self):
            return '{"id":"%s","content":"%s","page_type":"%s",status":"%s"}' %(self.id,self.content,self.page_type,self.status)
        
        