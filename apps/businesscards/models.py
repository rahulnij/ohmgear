from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.identifiers.models import Identifier
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.

class BusinessCardTemplate(models.Model):
    
        class Meta:
            db_table = 'ohmgear_businesscards_businesscardtemplate'
        template_name = models.CharField(_("Template Name"),max_length=50)
        template_content = models.CharField(_("Template Content"),max_length= 100)
        status  = models.IntegerField(_("Status"),default=0)
        created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
        updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
        
        def __unicode__(self):
            return '{"id":"%s","template_name":"%s","template_content":"%s"}' %(self.id,self.template_name,self.template_content)
    


class BusinessCard(models.Model):
    
    class Meta:
     db_table = 'ohmgear_businesscards_businesscard'
    name = models.CharField(_("name"),null=True,max_length=50)
     #----------- card type single or double----#
    bcard_type = models.IntegerField(_("Bussiness Card Type"),default=0)    
    #-----------Status denotes whether business card is published or not ----#
    status = models.IntegerField(_("Status"),default=0)
    #-----------is_active denotes whether business card is active or not----#
    is_active = models.IntegerField(_("Is Active"),default=1)
    #------------- Business Card Image both side ---------------------------#
    bcard_image_frontend = models.ImageField(_("Business Card Image Frontend"),upload_to='uploads/bcards_template_image/', max_length=254,blank=True,null=True)
    bcard_image_backend= models.ImageField(_("Business Card Image Backend"),upload_to='uploads/bcards_template_image/', max_length=254,blank=True,null=True)
    #------------- End ---------------------------#
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    user_id = models.ForeignKey(User,related_name='buser',db_column="user_id")
    
    def __unicode__(self):
        return'{"id:"%s","name":"%s"}'%(self.id,self.name)
  
    

class BusinessCardIdentifier(models.Model):
    
    class Meta:
        db_table = 'ohmgear_businesscards_identifier'
    businesscard = models.ForeignKey(BusinessCard)
    identifier = models.OneToOneField(Identifier)
    status      = models.IntegerField(_("Status"),default=1)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return'{"id:"%s","businesscard":"%s","identifier":"%s","status":"%s"}'%(self.id,self.businesscard,self.identifier,self.status)
    
class BusinessCardMedia(models.Model):
    
    class Meta:
        db_table = 'ohmgear_businesscards_media'
    user = models.ForeignKey(User)
    businesscard = models.ForeignKey(BusinessCard)
    img_url      = models.ImageField(_("Image Url"),default=1)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    position      = models.IntegerField(_("Position"),default=1) # 1=Horizontal ,2=Vertical
    status      = models.IntegerField(_("Status"),default=1)
    
    def __unicode__(self):
        return'{"id:"%s","businesscard":"%s","user":"%s","status":"%s"}'%(self.id,self.businesscard,self.user,self.status)
        
    
    