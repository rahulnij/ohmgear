import string
import random
import re

def CreateSystemIdentifier():
    serial = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
    return serial


# To Insert  Bulk Identifiers in database # 
#def CreateSystemIdentifier():
 #   insert_list = []    
  #  for i in range(100):
   #     identifier=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
    #    data  =insert_list.append(Identifier(identifier=identifier))
    #Identifier.objects.bulk_create(insert_list)


#def validate_identifier(identifier):
 #   letters = set(string.ascii_letters)
  #  digits = set(string.digits)
   # pwd = set(identifier)
    #return not (pwd.isdisjoint(letters) or pwd.isdisjoint(digits))
    
    





    
    
