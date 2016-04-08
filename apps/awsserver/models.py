from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


User = settings.AUTH_USER_MODEL


class AwsDeviceToken(models.Model):

    class Meta:
        db_table = 'ohmgear_aws_device_token'
        unique_together = ('device_token', 'user_id')

    deviceType = (
        ('apns', "Apple"),
        ('gcm', "Android"),

    )
    device_token = models.CharField(
        _('device token'),
        max_length=100,
        blank=True,
        null=True)
    aws_plateform_endpoint_arn = models.CharField(
        _('application endpoint arn'), max_length=150, blank=True, null=True)
    user_id = models.ForeignKey(
        User,
        null=False,
        db_column='user_id',
        related_name="user_aws_token")
    device_type = models.CharField(
        _('Device Type'),
        max_length=50,
        default='apns')
