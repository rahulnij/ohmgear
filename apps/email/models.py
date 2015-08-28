from django.db import models

# Create your models here.

EMAIL_TYPE = (
               ('1','user registration'),
               ('2','forgot password'),
             )
                
class EmailTemplate(models.Model):
    class Meta:
        db_table = 'ohmgear_emailtemplate'
    subject = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(_("Type"),max_length=45,choices=EMAIL_TYPE,default=1) 
    status = models.BooleanField()
    fromEmail = models.CharField(max_length=255)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=True)
    def __unicode__(self):
        return '{"id:"%s","subject":"%s","content":"%s","type":"%s"}'%(self.id,self.subject,self.content,self.type)
    
    
    
    
    
        
