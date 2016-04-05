from django.conf import settings
#------------------ Return token if does not exit then create -------------------#  
from ohmgear.functions import CustomeResponse
from serializer import GroupContactsSerializer
from models import GroupContacts
import rest_framework.status as status

def addFolderContact(group_contacts):
#    print "group_id"
#    print group_id
#    print "user_id"
#    print user_id
#    print "folder_contact_id"
#    print folder_contact_id
    print "group_contacts"
    print group_contacts
    user_id  =  group_contacts['user_id']
    print user_id
    group_id =  group_contacts['group_id'].id
    folder_contact_id = group_contacts['folder_contact_id']
    tempContainer = []
    for contacts in folder_contact_id:
             data = {}
             
             data['folder_contact_id'] = contacts
             data['group_id']          = group_id
             data['user_id']           = user_id
             group_contact_data_exist = GroupContacts(user_id=user_id,folder_contact_id=contacts,group_id=group_id)
             
             if group_contact_data_exist:
                 return CustomeResponse({'msg':'contact is already added with this user'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                 
             tempContainer.append(data)
             
    serializer = GroupContactsSerializer(data=tempContainer,many=True)
    if serializer.is_valid():
        serializer.save()
    
    
    