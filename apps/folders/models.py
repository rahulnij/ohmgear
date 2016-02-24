from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from apps.businesscards.models import BusinessCard
from apps.contacts.models import Contacts
from datetime import datetime

User = settings.AUTH_USER_MODEL

class FolderType(models.Model):
	class Meta:
		db_table = 'ohmgear_folders_foldertype'




class Folder(models.Model):
	class Meta:
		db_table = 'ohmgear_folders_folder'
	
	folderType = (
			('PR',"Private"),
		)
	foldername = models.CharField(_('folder name'), max_length=30,null=False,blank=False,error_messages={'blank':'Folder name can not be empty.'})
	foldertype = models.CharField(_('folder type'), max_length=2,null=False,blank=False,choices=folderType, default='PR')
	status = models.IntegerField(_('status'), default=1)
	user_id = models.ForeignKey(User,verbose_name=_('user'), null=False, db_column='user_id')
	businesscard_id =  models.ForeignKey(BusinessCard, verbose_name= _('business card'), null=True,blank=True,db_column='businesscard_id')
	created_date = models.DateTimeField(_('created date'),default=datetime.now,blank=True)
	updated_date =  models.DateTimeField(_('updated date'),default=datetime.now,blank=True)

	def __unicode__(self):
		return '{"id":%d,"foldername":%s,"foldertype":%s }' %(self.id,self.foldername,self.foldertype)
            

class FolderContact(models.Model):
	class Meta:
		db_table = 'ohmgear_folders_folder_contact'
               
        linkStatus = (
			(0,"White"),
                        (1,"Green"),
                        (2,"Blue"),
                        (3,"Orange"),
		     )        

        user_id = models.ForeignKey(User, null=False, db_column='user_id')
        
        folder_id = models.ForeignKey(Folder, db_column='folder_id')
	contact_id = models.ForeignKey(Contacts,db_column='contact_id',related_name='folder_contact_data')
        link_status =  models.IntegerField(_('link_status'), default=0,choices=linkStatus)
	is_linked = models.IntegerField(_('status'), default=0)
        
        created_date = models.DateTimeField(_('created date'),auto_now_add=True,auto_now=False)
	updated_date =  models.DateTimeField(_('updated date'),auto_now_add=False,auto_now=True)

	def __unicode__(self):
		return '{"folder_id":%d,"contact_id":%d,"link_status":%d,"is_linked":%d}' %(self.folder_id.id,self.contact_id.id,self.link_status,self.is_linked)            
