from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
# Create your models here.
              
class EmailTemplate(models.Model):
    class Meta:
        db_table = 'ohmgear_email_emailtemplate'
    subject = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField() 
    status = models.BooleanField()
    from_email = models.CharField(max_length=255,default='')
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=True)
    
    def __unicode__(self):
        return '{"id:"%s","subject":"%s","content":"%s","slug":"%s"}'%(self.id,self.subject,self.content,self.slug)

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.s = slugify(self.slug)
        super(EmailTemplate, self).save(*args, **kwargs)    
    
    
    
    
    
        
