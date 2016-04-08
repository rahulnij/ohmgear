from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your models here.


class SendRequest(models.Model):

    class Meta:
        db_table = 'ohmgear_send_request'

    AcceptedStatus = (
        (0, "sent"),
        (1, "accepted"),
        (2, "not accepted")
    )

    RequestType = (
        ("b2b", "bcard to bcard"),
        ("b2g", "bcard to grey card"),
    )
    type = models.CharField(max_length=50, default="b2b", choices=RequestType)

    sender_user_id = models.ForeignKey(
        User,
        db_column="sender_user_id",
        related_name='srequest_sender_user_id')
    sender_obj_id = models.PositiveIntegerField(default=0, blank=True)

    receiver_user_id = models.ForeignKey(
        User,
        db_column="receiver_user_id",
        related_name='srequest_receiver_user_id',
        null=True,
        blank=True)
    receiver_obj_id = models.PositiveIntegerField(default=0, blank=True)

    message = models.CharField(max_length=200, blank=True, null=True)
    read_status = models.BooleanField(default=0)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateField(
        _("Updated Date"), auto_now_add=False, auto_now=True)
