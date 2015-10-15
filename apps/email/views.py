from django.shortcuts import render
from rest_framework.reverse import reverse
from django.conf import settings
from django.core.mail import send_mail
from apps.email.models import EmailTemplate
from celery.task import Task
from celery.registry import tasks
#-------- Send all types of mail here ---------------------#
# userObje: It have all information about user whom email will go
# type: which type of email you are sending to individual
class BaseSendMail(Task):
    def run(self,userObj,type,**kwargs):
        if type:
           try: 
            email=EmailTemplate.objects.get(slug=type)
           except:
            return False
           
           if type == 'account_confirmation':
               
                activation_key = kwargs.get("key")
                email_body = email.content.replace('%user_name%',userObj['first_name'])
                url = reverse('registration_confirm', args=[activation_key])
                email_body = email_body.replace('%url%',"<a href='"+settings.DOMAIN_NAME+url+"'>Link</a>")

           elif type == 'forgot_password': 
               
                reset_password_key = kwargs.get("key")
                email_body = email.content.replace('%user_name%',userObj['first_name'])
                url = reverse('forgot_password', args=[reset_password_key])
                email_body = email_body.replace('%url%',"<a href='"+settings.DOMAIN_NAME+url+"'>Link</a>")
                
           email.from_email = email.from_email if email.from_email else settings.DEFAULT_FROM_EMAIL
           send_mail(email.subject, email_body, email.from_email,
                            [userObj['email']], fail_silently=False,html_message=email_body) 
                        
#-------- End ---------------------------------------------#

#------------------- Register the task --------------------#
tasks.register(BaseSendMail)
#-------------------- End ---------------------------------#
