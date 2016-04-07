import datetime
from datetime import timedelta
from django.utils.timezone import utc
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from serializer import ConnectedAccountsSerializer
from models import ConnectedAccount, SocialType, User
import random

#------------------ Return token if does not exit then create -------------------#


def getToken(user_id):

    if user_id:
        #----------- first check previous token if exist then delete -----------#
        try:
            token = Token.objects.get(user_id=user_id)
            token.delete()
        except:
            pass
        try:
            token = Token()
            token.user_id = user_id
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
            user = get_user_model().objects.filter(
                email=email_id, user_type__in=[2, 3]).values()
            user[0].pop('password')
            return user
        except:
            return None
    else:
        return None


def createConnectedAccount(user_id, social_type_id):

    try:
        connecteddata = ConnectedAccount.objects.filter(
            user_id=user_id, social_type_id=social_type_id)

        if not connecteddata:
            user_id = User.objects.get(id=user_id)
            social_type_id = SocialType.objects.get(id=social_type_id)
            connectedaccount = ConnectedAccount()
            connectedaccount.user_id = user_id
            connectedaccount.social_type_id = social_type_id
            connectedaccount.save()
            return connectedaccount
        else:
            return None
    except:
        return None


def CreatePinNumber():
    pin_no = ''.join(random.choice('0123456789') for i in range(4))
    try:
        pin_no_exist = User.objects.get(pin_number=pin_no)
    except:
        pin_no_exist = ''

    if pin_no_exist:
        return CreatePinNumber()
    return pin_no
