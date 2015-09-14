#----------------------------------------------#
# Developer Name: Sajid
# Creation Date: 2015/08/12
# Notes: View File
#----------------------------------------------#
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from models import User,Profile
from apps.email.views import base_send_mail
import hashlib, datetime, random
#---------------------------- Create profile at the time of registration --------------------------#
def register_profile(sender, **kwargs):  
    if kwargs.get('created'):
        user = kwargs.get('instance')
        request = kwargs.get("request")
        if user.id is not None and user._disable_signals is not True:
                profile = Profile(user=user)
                if user.status is not 1:
                    #------------------- Send the registration mail to user and it have confirmation link ----------#
                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                    activation_key = hashlib.sha1(salt+user.email).hexdigest()            
                    key_expires = datetime.datetime.today() + datetime.timedelta(2)

                    base_send_mail(user,type='account_confirmation',activation_key = activation_key)

                    profile.activation_key = activation_key
                    profile.key_expires = key_expires
                #--------------------- End -------------------------------------------------------------#

                profile.save()
                return
post_save.connect(register_profile, sender=User, dispatch_uid='register_profile')
#-------------------------- End ---------------------------------------------------------------------#
