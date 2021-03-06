from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL


class VacationCard(models.Model):

    class Meta:
        db_table = 'ohmgear_vacationcard_vacationcard'
    vacation_name = models.CharField(_('Vacation Name'), max_length=100)
    user_id = models.ForeignKey(
        User, db_column="user_id", related_name='user_vacationcard', null=True)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
    status = models.IntegerField(_('Status'), default=1)

    def __unicode__(self):
        return'{"id":"%s","user_id":"%s"}' % (self.id, self.user_id.id)


class VacationTrip(models.Model):

    class Meta:
        db_table = 'ohmgear_vacationcard_vacationtrip'

    country = models.CharField(
        _('Country'), max_length=50, null=True, blank=True)
    vacation_type = models.CharField(_('Vaction Type'), max_length=100)
    state = models.CharField(_('State'), max_length=50, null=True, blank=True)
    city = models.CharField(_('City'), max_length=50, null=True, blank=True)
    contact_no = models.CharField(
        _("Contact Number"), max_length=50, null=True, blank=True)
    notes = models.CharField(
        _('Notes'), max_length=2000, null=True, blank=True)
    user_id = models.ForeignKey(User, db_column="user_id", null=True)
    trip_start_date = models.DateField(_('Trip Start Date'))
    trip_end_date = models.DateField(_('Trip End Date'))
    vacationcard_id = models.ForeignKey(
        VacationCard, db_column="vacationcard_id", related_name="vacation_trips")
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
    status = models.IntegerField(_('Status'), default=1)

    def __unicode__(self):
        return '{"id":"%s","country":"%s","vacation_type":"%s","state":"%s","contact_no":"%s","notes":"%s","trip_start_date":"%s","trip_end_date":"%s","vacationcard_id":"%s"}' % (self.id, self.country, self.vacation_type, self.state, self.contact_no, self.notes, self.trip_start_date, self.trip_end_date, self.vacationcard_id)
