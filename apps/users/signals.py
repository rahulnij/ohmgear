# ---------------------------------------------- #
# Developer Name: Sajid
# Creation Date: 2015/08/12
# ---------------------------------------------- #

import sys

from django.db.models.signals import post_save, pre_save
from django.forms.models import model_to_dict
from django.dispatch import receiver

from models import Profile
from apps.email.views import BaseSendMail


# Create profile at the time of registration


def register_profile(sender, **kwargs):
    if kwargs.get('created'):
        profile = kwargs.get('instance')
        if profile:
            user_new = model_to_dict(profile.user)
            try:
                # condition for not calling at the time of run test cases
                if not 'test' in sys.argv:
                    BaseSendMail.delay(
                        user_new,
                        type='account_confirmation',
                        key=profile.activation_key)
            except:
                pass
            return
post_save.connect(register_profile, sender=Profile,
                  dispatch_uid='register_profile')
# -------------------------- End ------------------------ #


@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = Profile.objects.get(pk=instance.pk)
        if instance.profile_image and existing_image.profile_image != instance.profile_image:
            existing_image.profile_image.delete(False)
