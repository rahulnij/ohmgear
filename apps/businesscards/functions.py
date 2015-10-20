import datetime
from datetime import timedelta
from django.utils.timezone import utc
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
#------------------ Return token if does not exit then create -------------------#  
def getToken(user_id):
    
    if user_id:
        #----------- first check previous token if exist then delete -----------#
        try:
            token = Token.objects.get(user_id = user_id)
            token.delete()
        except:
            pass
        try:
            token =  Token()
            token.user_id =  user_id
            token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
            token.save()
            return token.key
        except:
            return None
        #------------------ End -----------------------------------#        
    else:
        return None
    
    
#------------------ Return token if does not exit then create -------------------#  
def checkEmail(email_id):
    
    if email_id:
        try:
            user = get_user_model().objects.filter(email=email_id,user_type__in=[2,3]).values()
            user[0].pop('password')
            return user
        except:
            return None
    else:
        return None    
    
    