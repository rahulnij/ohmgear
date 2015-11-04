from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django.db.models.User import User
from apps.businesscards.models import BusinessCard
from django.conf import settings
User = settings.AUTH_USER_MODEL


class VacationCard(models.Model):
    class Meta:
        db_table  = 'ohmgear_vacationcard_vacationcard'
    user_id            =   models.ForeignKey(User,db_column ="user_id")
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    status          =   models.IntegerField(_('Status'),default =1)
    
    def __unicode__(self):
        return'{"id":"%s","user_id":"%s"}'%(self.id,self.user_id)
    
    
    
class BusinessCardVacation(models.Model):
    class Meta:
        db_table = 'ohmgear_vacationcard_businesscardvacation'
        unique_together = ('user_id', 'businesscard_id')
        
    vacationcard_id    =   models.ForeignKey(VacationCard,db_column ="vacationcard_id")
    businesscard_id    =   models.ForeignKey(BusinessCard,db_column = "businesscard_id")
    user_id         =   models.ForeignKey(User,db_column = "user_id")
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    status                  =   models.IntegerField(_('Status'),default =1)
        
    def __unicode__(self):
        return '{"id":"%s","vacationcard","businesscard":"%s"}'%(self.id,self.vacationcard,self.businesscard)
    
    
class VacationTrip(models.Model):
    class Meta:
        db_table = 'ohmgear_vacationcard_vacationtrip'
        
    country         =   models.CharField(_('Country'),max_length=50)
    state           =   models.CharField(_('State'),max_length=50)
    contact_no      = models.CharField(_("Contact Number"),max_length=10,null=True)
    notes           =   models.CharField(_('Notes'),max_length = 2000)
    user_id         =   models.ForeignKey(User,db_column="user_id")
    trip_start_date =   models.DateField(_('Trip Start Date'))
    trip_end_date   =   models.DateField(_('Trip End Date'))
    vacationcard_id    =   models.ForeignKey(VacationCard,db_column ="vacationcard_id")
    created_date=models.DateTimeField(_("Created Date"),auto_now_add=True,auto_now=False)
    updated_date=models.DateTimeField(_("Updated Date"),auto_now_add=False,auto_now=True)
    status          =   models.IntegerField(_('Status'),default =1)
        
    def __unicode__(self):
        return '{"id":"%s","country","state":"%s","contact_no":"%s","notes":"%s","trip_start_date":"%s","trip_end_date"}'%(self.id,self.country,self.state,self.contact_no,self.notes,self.trip_start_date,self.trip_end_date)
        
    