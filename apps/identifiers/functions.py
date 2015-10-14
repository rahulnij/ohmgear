import random
from models import Identifier

#def CreateSystemIdentifier():
 #   serial = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
  #  return serial



def CreateSystemIdentifier():
    insert_list = []    
    for i in range(100):
        identifier=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
        data  =insert_list.append(Identifier(identifier=identifier))
    Identifier.objects.bulk_create(insert_list)

    
    