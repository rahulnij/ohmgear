from django.conf import settings
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
  
    
    