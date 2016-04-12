# Standard library imports
from django.conf import settings
from rest_framework.reverse import reverse
from django.core.mail import send_mail

# Third party imports
from celery.task import Task
from celery.registry import tasks

# local app imports
from apps.email.models import EmailTemplate
from apps.users.models import Profile

"""
    Send all types of mail
    user: It have all information about user whom email will go
    type: which type of email you are sending to individual
"""


class BaseSendMail(Task):

    def run(self, user, type, **kwargs):
        if type:
            try:
                if type != 'test_email': 
                    email = EmailTemplate.objects.get(slug=type)
            except:
                return False

            if type != 'grey_invitation' and type != 'test_email':
                    user_id = user['id']
                    getdata = Profile.objects.get(user=user_id)

            if type == 'account_confirmation':

                user_id = user['id']
                getdata = Profile.objects.get(user=user_id)
                activation_key = kwargs.get("key")

                email_subject = email.subject
                email_body = email.content.replace(
                    '%user_name%', getdata.first_name)
                url = '/api/useractivity/?activation_key=' + \
                    str(activation_key)
                email_body = email_body.replace(
                    '%url%', "<a href='" + settings.DOMAIN_NAME + url + "'>Link</a>")

            if type == 'verify_email':

                activation_key = kwargs.get("key")

                email_subject = email.subject
                email_body = email.content.replace(
                    '%user_name%', str(getdata.first_name))
                url = '/api/users/emails/verify_email/?activation_code=' + \
                    str(activation_key)
                email_body = email_body.replace(
                    '%url%', "<a href='" + settings.DOMAIN_NAME + url + "'>Link</a>")

            if type == 'grey_invitation':

                activation_key = kwargs.get("key")
                user['email'] = str(kwargs.get(
                    "email")).decode('base64', 'strict')
                first_name = str(kwargs.get("first_name")
                                 ).decode('base64', 'strict')
                email_subject = email.subject
                email_body = email.content.replace('%user_name%', first_name)
                url = kwargs.get('url')
                email_body = email_body.replace(
                    '%url%', "<a href='" + url + "'>Link</a>")

            elif type == 'forgot_password':
                
                reset_password_key = kwargs.get("key")
                email_subject = email.subject
                email_body = email.content.replace(
                    '%user_name%', getdata.first_name)
                url = reverse('forgot_password', args=[reset_password_key])
                email_body = email_body.replace(
                    '%url%', "<a href='" + settings.DOMAIN_NAME + url + "'>Link</a>")

            elif type == 'test_email':
                # ------- not getting fixture default data here ------- #
                email_subject = 'testing mail'
                email_body = "Hey this is test mail from kinbow."

            try:
                from_email = email.from_email if email.from_email else settings.DEFAULT_FROM_EMAIL
            except:
                from_email = ''   

            send_mail(email_subject,
                      email_body,
                      from_email,
                      [user['email']],
                      fail_silently=False,
                      html_message=email_body)


# Registered the task
tasks.register(BaseSendMail)
