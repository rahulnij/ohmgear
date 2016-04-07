from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from simple_history.models import HistoricalRecords
from django_pgjson.fields import JsonField
User = settings.AUTH_USER_MODEL

#from serializer import BusinessCardMediaSerializer
# Create your models here.


class Feedbacks(models.Model):

    class Meta:
        db_table = 'ohmgear_feedback'
    user_id = models.ForeignKey(User, db_column="user_id")
    bug_type = models.CharField(_("Bug Type"), max_length=50)
    comment = models.TextField(_("Comment"), max_length=50)
    status = models.IntegerField(_("Status"), default=1)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","user_id":"%s","comment":"%s",bug_type":"%s"}' % (self.id, self.user_id, self.comment, self.bug_type)


class FeedbackCategory(models.Model):

    class Meta:
        db_table = 'ohmgear_feedback_feedbackcategory'
    category_name = models.CharField(
        _("Category Name"), max_length=255, null=True)
    status = models.IntegerField(_("Status"), default=1)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Update Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","category_name":"%s"}' % (self.id, self.category_name)


class FeedbackCategorySubject(models.Model):

    class Meta:
        db_table = 'ohmgear_feedback_feedbackcategorysubject'
    feedback_category_id = models.ForeignKey(
        FeedbackCategory, db_column="feedback_category_id")
    subject_text = models.CharField(_("Subject"), max_length=255, null=True)
    status = models.IntegerField(_("Status"), default=1)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Update Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","subject_text":"%s"}' % (self.id, self.subject_text)


class ContactUs(models.Model):

    class Meta:
        db_table = 'ohmgear_feedback_contactus'
    user_id = models.ForeignKey(User, db_column='user_id')
    feedback_category_id = models.ForeignKey(
        FeedbackCategory, db_column="feedback_category_id")
    feedback_category_subject_id = models.ForeignKey(
        FeedbackCategorySubject, db_column="feedback_category_subject_id")
    description = models.TextField("Description")
    file_name = models.FileField(
        _("File Name"), upload_to='uploads/contact_file/', max_length=254)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return '{"id":"%s","feedback_category_id":"%s","feedback_category_subject_id":"%s","description":"%s"}' % (self.id, self.feedback_category_id, self.feedback_category_subject_id, self.description)
