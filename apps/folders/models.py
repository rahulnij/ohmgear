from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from apps.businesscards.models import BusinessCard
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
	businesscard =  models.ForeignKey(BusinessCard, verbose_name= _('business card'), null=False, on_delete=models.CASCADE, db_column='businesscard_id')
	created_date = models.DateTimeField(_('created date'),default=datetime.now,blank=True)
	updated_date =  models.DateTimeField(_('updated date'),default=datetime.now,blank=True)

	def __unicode__(self):
		return '{"foldername":%s,"foldertype":%s }' %(self.foldername,self.foldertype)
