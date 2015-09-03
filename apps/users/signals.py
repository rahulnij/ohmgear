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
        if user.id is not None:
                profile = Profile(user=user)                
                
                #------------------- Send the registration mail to user and it have confirmation link ----------#
                salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                activation_key = hashlib.sha1(salt+user.email).hexdigest()            
                key_expires = datetime.datetime.today() + datetime.timedelta(2)
                
                email=EmailTemplate.objects.get(type__slug='account_confirmation')
                if email:
                    email_body = email.content.replace('%user_name%',user.first_name)
                    url = reverse('registration_confirm', args=[activation_key])
                    email_body = email_body.replace('%url%',"<a href='"+settings.DOMAIN_NAME+url+"'>Link</a>")
                    email.fromEmail = email.fromEmail if email.fromEmail else setting.DEFAULT_FROM_EMAIL
                    
                    send_mail(email.subject, email_body, email.fromEmail,
                                    [user.email], fail_silently=False,html_message=email_body)                   
                else:
                   pass 
                #--------------------- End -------------------------------------------------------------#
                profile.activation_key = activation_key
                profile.key_expires = key_expires
                profile.save()
                return
post_save.connect(register_profile, sender=User, dispatch_uid='register_profile')
#-------------------------- End ---------------------------------------------------------------------#
