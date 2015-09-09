#----------------------------------------------#
# Developer Name: Sajid
# Creation Date: 2015/08/12
# Notes: View File
#----------------------------------------------#
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from models import User,Profile
from apps.email.models import EmailTemplate
import hashlib, datetime, random
from rest_framework.reverse import reverse
from django.conf import settings
from django.core.mail import send_mail

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

                    email=EmailTemplate.objects.get(slug='account_confirmation')
                    if email:
                        email_body = email.content.replace('%user_name%',user.first_name)
                        url = reverse('registration_confirm', args=[activation_key])
                        #url = 'signUpEmailVerification://?activationKey='+str(activation_key)
                        email_body = email_body.replace('%url%',"<a href='"+url+"'>Link</a>")
                        email.from_email = email.from_email if email.from_email else settings.DEFAULT_FROM_EMAIL

                        send_mail(email.subject, email_body, email.from_email,
                                        [user.email], fail_silently=False,html_message=email_body)                   
                    else:
                       pass 
                    profile.activation_key = activation_key
                    profile.key_expires = key_expires
                #--------------------- End -------------------------------------------------------------#

                profile.save()
                return
post_save.connect(register_profile, sender=User, dispatch_uid='register_profile')
#-------------------------- End ---------------------------------------------------------------------#
