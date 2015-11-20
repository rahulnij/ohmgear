from django.shortcuts import render
import rest_framework.status as status
import json,jsonschema
from rest_framework.decorators import api_view
from ohmgear.functions import CustomeResponse

from serializer import ContactsSerializer,ContactsSerializerWithJson
from ohmgear.json_default_data import BUSINESS_CARD_DATA_VALIDATION
import validictory
# Create your views here.

#--------------------- Storing Contacts as a Bulk -----------------------#
@api_view(['GET','POST'])       
def storeContacts(request,**kwargs):
    if request.method == 'GET':
        return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
    if request.method == 'POST':
        # ----------- Login ------------------#
        op = request.POST.get('op','')
        if op == 'save_contact':
             NUMBER_OF_CONTACT = 100
             try:
              contact = json.loads(request.DATA['contact'])
             except:
               return CustomeResponse({'status':'fail','msg':'Please provide correct Json Format'},status=status.HTTP_400_BAD_REQUEST)
            
             if contact:
               counter = 0  
               for contact_temp in contact:
                    print contact_temp
                    #--------------------  Validate the json data ------------------------------#
                    try:
                       validictory.validate(contact_temp["bcard_json_data"], BUSINESS_CARD_DATA_VALIDATION)
                    except validictory.ValidationError as error:
                       return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                    except validictory.SchemaError as error:
                       return CustomeResponse({'msg':error.message },status=status.HTTP_400_BAD_REQUEST,validate_errors=1)        
                    #---------------------- - End ----------------------------------------------------------- #
                    counter = counter + 1
                    
               if counter > NUMBER_OF_CONTACT:
                    return CustomeResponse({'msg':"Max "+str(NUMBER_OF_CONTACT)+" allowed to upload"},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
               serializer = ContactsSerializer(data=contact,many=True)
               if serializer.is_valid():
                serializer.save()
                return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
               else:
                return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)   
        else:
             return CustomeResponse({'msg':'Please provide operation parameter op'},status=status.HTTP_401_UNAUTHORIZED,validate_errors=1)            
