# --------- Import Python Modules ----------- #
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

# ----------------- Local app imports ------ #


from apps.identifiers.models import Identifier
from simple_history.models import HistoricalRecords
from apps.vacationcard.models import VacationCard

User = settings.AUTH_USER_MODEL


class BusinessCardTemplate(models.Model):

    class Meta:
        db_table = 'ohmgear_businesscards_businesscardtemplate'
    template_name = models.CharField(_("Template Name"), max_length=50)
    template_content = models.CharField(_("Template Content"), max_length=50)
    status = models.IntegerField(_("Status"), default=0)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","template_name":"%s","template_content":"%s"}' % (
            self.id, self.template_name, self.template_content)


class BusinessCard(models.Model):

    class Meta:
        db_table = 'ohmgear_businesscards_businesscard'
    name = models.CharField(_("name"), null=True, max_length=50)
    # card type single or double
    bcard_type = models.IntegerField(_("Bussiness Card Type"), default=0)
    # Status denotes whether business card is published or not
    status = models.IntegerField(_("Status"), default=0)
    # is_active denotes whether business card is active or not
    is_active = models.IntegerField(_("Is Active"), default=1)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
    user_id = models.ForeignKey(
        User, related_name='buser', db_column="user_id")

    business_identifier = models.ManyToManyField(
        Identifier,
        through='BusinessCardIdentifier',
        related_name='business_identifier')
    business_vacation = models.ManyToManyField(
        VacationCard,
        through='BusinessCardVacation',
        related_name='business_vacation')
    history = HistoricalRecords()

    def __unicode__(self):
        return'{"id":"%s","name":"%s","user_id":"%s","is_active":"%s"}' % (self.id, self.name, self.user_id.id, self.is_active)


class BusinessCardIdentifier(models.Model):

    class Meta:
        db_table = 'ohmgear_businesscards_identifier'

    businesscard_id = models.ForeignKey(
        BusinessCard, db_column="businesscard_id", related_name='identifiers_data')
    identifier_id = models.OneToOneField(
        Identifier,
        db_column="identifier_id",
        related_name='businesscard_identifiers'
    )
    status = models.IntegerField(_("Status"), default=1)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return'{"id":"%s","businesscard_id":"%s","identifier_id":"%s","status":"%s"}' % \
            (self.id, self.businesscard_id, self.identifier_id, self.status)

    def bcard_data(self):
        bcarddata = BusinessCard.objects.filter(id=self.id)
        data = []

        for item in bcarddata:
            data.append({"name": item.name, "bcard_type": item.bcard_type})
        return data


class BusinessCardSkillAvailable(models.Model):

    class Meta:
        db_table = 'ohmgear_businesscards_businesscardavailableskills'

    skill_name = models.CharField(_("Skill Name"), null=True, max_length=50)
    status = models.IntegerField(_("Status"), default=1)

    def __unicode__(self):
        return'{"id":"%s","skillset":"%s"}' % (self.id, self.skill_name)


class BusinessCardAddSkill(models.Model):

    class Meta:
        db_table = 'ohmgear_businesscards_businesscardaddskills'
    user_id = models.ForeignKey(User, db_column="user_id")
    businesscard_id = models.ForeignKey(
        BusinessCard,
        db_column='businesscard_id',
        related_name='businesscard_skills')
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
    skill_name = models.TextField("Skill Name")

    status = models.IntegerField(_("Status"), default=1)

    def __unicode__(self):
        return'{"id":"%s","businesscard_id":"%s","skillname":"%s"}' % (self.id, self.businesscard_id, self.skill_name)


class BusinessCardVacation(models.Model):

    class Meta:
        db_table = 'ohmgear_vacationcard_businesscardvacation'
        unique_together = ('vacationcard_id', 'businesscard_id')

    vacationcard_id = models.ForeignKey(
        VacationCard,
        db_column="vacationcard_id",
        related_name="businesscardvacation")
    businesscard_id = models.ForeignKey(
        BusinessCard, db_column="businesscard_id")
    user_id = models.ForeignKey(User, db_column="user_id")
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
    status = models.IntegerField(_('Status'), default=1)

    def __unicode__(self):
        return '{"id":"%s","vacationcard_id","businesscard_id":"%s"}' % (
            self.id, self.vacationcard_id, self.businesscard_id)
