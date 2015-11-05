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
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    user_id = models.ForeignKey(User,related_name='buser',db_column="user_id")
    
    
    identifier_new = models.ManyToManyField(Identifier, through = 'BusinessCardIdentifier',related_name='identifier_new')
    
    def __unicode__(self):
        return'{"id":"%s","name":"%s"}' %(self.id,self.name)
  
    

class BusinessCardIdentifier(models.Model):
    
    class Meta:
        db_table = 'ohmgear_businesscards_identifier'
    businesscard_id = models.ForeignKey(BusinessCard,db_column="businesscard_id")
    identifier_id = models.OneToOneField(Identifier,db_column="identifier_id",related_name='businesscard_identifiers')
    status      = models.IntegerField(_("Status"),default=1)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return'{"id:"%s","businesscard_id":"%s","identifier_id":"%s","status":"%s"}' %(self.id,self.businesscard_id,self.identifier_id,self.status)
    
class BusinessCardMedia(models.Model):
    
    class Meta:
        db_table = 'ohmgear_businesscards_media'
    user_id = models.ForeignKey(User,db_column="user_id")
    businesscard_id = models.ForeignKey(BusinessCard,db_column='businesscard_id')
    img_url      = models.ImageField(_("Image Url"),upload_to='uploads/bcards_gallary/', max_length=254)
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    front_back      = models.IntegerField(_("Front Back"),default=1) # 1=Front ,2=Back
    position      = models.IntegerField(_("Position"),default=1) # 1=Horizontal ,2=Vertical
    status      = models.IntegerField(_("Status"),default=0)
    
    def __unicode__(self):
        return '{"id:"%s","businesscard_id":"%s","user_id":"%s","status":"%s","front_back":"%s","img_url":"%s"}' %(self.id,self.businesscard_id,self.user_id,self.status,self.front_back,self.img_url)
        
    
class BusinessCardSkillAvailable(models.Model):
    
    class Meta:
        db_table = 'ohmgear_businesscards_businesscardavailableskills'
    skill_name = models.CharField(_("Skill Name"),null=True,max_length=50)
    status      = models.IntegerField(_("Status"),default=1)
    
    def __unicode__(self):
        return'{"id:"%s","skillset":"%s"}'%(self.id,self.skill_name)
  
class BusinessCardAddSkill(models.Model):
    
    class Meta:
        db_table = 'ohmgear_businesscards_businesscardaddskills'
    #user = models.ForeignKey(User)
    user_id = models.ForeignKey(User,db_column="user_id")
    businesscard_id = models.ForeignKey(BusinessCard,db_column='businesscard_id',related_name='businesscard_skills')
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    skill_name = models.CharField(_("Skill Name"),null=True,max_length=50)
    status      = models.IntegerField(_("Status"),default=1)
    
    def __unicode__(self):
        return'{"id:"%s","businesscard_id":"%s","skillname":"%s"}' %(self.id,self.businesscard_id,self.skill_name)
            