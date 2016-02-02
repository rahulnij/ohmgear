from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.
class Setting(models.Model):
    
    class Meta:
        db_table = 'ohmgear_user_setting_setting'
    key =   models.CharField(_("Key"),unique=True,max_length=100)
    default_value   =   models.CharField(_("Default Value"),max_length=50)
    value_type      =   models.CharField(_("Value Type"),max_length=10)
    created_date    =   models.DateTimeField(_("Created Date"),auto_now_add =True,auto_now=False)
    updated_date    =   models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return'{"id":"%s","key":"%s","value_type":"%s"}' %(self.id,self.key,self.value_type)
    
    
    
class UserSetting(models.Model):
    
    class Meta:
        unique_together = ('user_id', 'setting_id')
        db_table    =   'ohmgear_user_setting_user_setting'
    user_id         =   models.ForeignKey(User,db_column="user_id")
    setting_id      =   models.ForeignKey(Setting,db_column="setting_id",related_name= "setting_data")
    value           =   models.CharField(_("Value"),max_length=50)
    created_date    =   models.DateTimeField(_("Created Date"),auto_now_add =True,auto_now=False)
    updated_date    =   models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return'{"id":"%s","user_id":"%s","setting_id":"%s","value":"%s"}' %(self.id,self.user_id,self.setting_id,self.value)
    
    
class Language(models.Model):
    
    class Meta:
        db_table    =   'ohmgear_user_setting_language'
    language    =   models.CharField(_("Language"),max_length=50)
    created_date    =   models.DateTimeField(_("Created Date"),auto_now_add =True,auto_now=False)
    updated_date    =   models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return'{"id":"%s","language":"%s"}' %(self.id,self.language)
        
        
class DisplayContactNameAs(models.Model):
    
    class Meta:
        db_table    =   'ohmgear_user_setting_display_contact_name_as'
    name_display_format    =   models.CharField(_("Name Display Format"), max_length=100)
    created_date    =   models.DateTimeField(_("Created Date"),auto_now_add =True,auto_now=False)
    updated_date    =   models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    
    def __unicode__(self):
        return'{"id":"%s","name_display_format":"%s"}' %(self.id,self.name_display_format)
    