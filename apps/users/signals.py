# ---------------------------------------------- #
# Developer Name: Sajid
# Creation Date: 2015/08/12
import sys

from django.db.models.signals import post_save, pre_save, pre_delete
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist
from apps.groups.models import GroupMedia
# TODO, move image to common lib
# from common.image_lib import resize_image, MAX_WIDTH
from django.dispatch import receiver

from models import Profile
from apps.email.views import BaseSendMail

from django.conf import settings


from logging import getLogger

log = getLogger(__name__)


# Create profile at the time of registration

def register_profile(sender, **kwargs):
    if kwargs.get('created'):
        profile = kwargs.get('instance')
        if profile:
            user_new = model_to_dict(profile.user)
            try:
                # condition for not calling at the time of run test cases
                if 'test' not in sys.argv:
                    BaseSendMail.delay(
                        user_new,
                        type='account_confirmation',
                        key=profile.activation_key)
            except:
                pass
            return
post_save.connect(register_profile, sender=Profile,
                  dispatch_uid='register_profile')
# End


@receiver(post_save, sender=Profile)
def resize_profile_image(sender, instance, *args, **kwargs):
    try:
        obj = Profile.objects.get(pk=instance.pk)
        """
        Rahul: image_path(i think you might need this "profile_image:)
        not exists please correct this.
        Till then i have commented this code
        """
        if obj.profile_image.name:
            img_resized = resize_image(
                settings.BASE_DIR + str(obj.profile_image.url), MAX_WIDTH)
            obj.image_path = img_resized
            try:
                obj.save()
            except Exception as e:
                log.critical(
                    "Unhandled exception in {}, {}".format(
                        __name__, e))
                # TODO, notify Sentry
    except ObjectDoesNotExist as e:
        log.error("Exception getting profile object: {}".format(e))
        # TODO, notify Sentry


@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = Profile.objects.get(pk=instance.pk)
        if instance.profile_image and existing_image.profile_image != instance.profile_image:
            existing_image.profile_image.delete(False)


@receiver(pre_delete, sender=GroupMedia)
def delete_old_group_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = GroupMedia.objects.get(pk=instance.pk)
        if instance.img_url or existing_image.img_url != instance.img_url:
            existing_image.img_url.delete(False)
