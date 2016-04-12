import string
import random
from models import Identifier, LockIdentifier
import re


def CreateSystemIdentifier():
    serial = ''.join(random.choice(
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(5))
    region = "I"
    serialregion = region + serial
    identifier_exist = Identifier.objects.filter(
        identifier=serialregion).values()
    identifier_lock = LockIdentifier.objects.filter(
        identifier=serialregion).values()
    if identifier_exist or identifier_lock:
        return CreateSystemIdentifier()
    return serialregion


def validate_identifier(identifier):

    if re.match(r'^[A-Za-z0-9^&]{6,12}$', identifier):
        return True
    else:
        return False
