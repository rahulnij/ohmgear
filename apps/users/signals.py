#----------------------------------------------#
# Developer Name: Sajid
# Creation Date: 2015/08/12
# Notes: View File
#----------------------------------------------#
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from models import User,Profile

#---------------------------- Create profile at the time of registration --------------------------#
def register_profile(sender, *args, **kwargs):  
    if kwargs.get('created'):
        user = kwargs.get('instance')
        if user.id is not None:
                profile = Profile(user=user)
                profile.save()
                return
post_save.connect(register_profile, sender=User, dispatch_uid='register_profile')
#-------------------------- End ---------------------------------------------------------------------#
