from django.conf import settings
#------------------ Return token if does not exit then create -------------------#  
from models import VacationCard,VacationTrip
from serializer import VacationTripSerializer
from ohmgear.functions import CustomeResponse
import rest_framework.status as status

def CreateDuplicateVacationCard(vacation_id=None,user_id=None):
    
    if vacation_id and user_id:
            
            #-------------------- Duplicate Vacation card row ---------------------------# 
            try:
             vcards = VacationCard.objects.get(id=vacation_id,user_id=user_id)
            except:
              return None  
            vcards.id = None
            vcards.save()
            vcards_id_new = vcards.id
            #---------------------- End---------------------------------------------------#
            
            #--------------------- Duplicate Vacation Trip row ------------------------#
            try:
            
                vacation_trip = VacationTrip.objects.filter(vacationcard_id=vacation_id).values()


                if vacation_trip and vcards_id_new:
                    tempContainer = []
                    for data in vacation_trip:
                        data.pop("user_id_id")
                        data.pop("vacationcard_id_id")
                        data.pop('created_date')
                        data.pop('updated_date')
                        tempdata = {}

                        tempdata =   data
                        tempdata['vacationcard_id'] = vcards_id_new
                        tempdata['user_id']    =        user_id.id
                        tempContainer.append(tempdata)
                    serializer = VacationTripSerializer(data=tempContainer,many=True)
                    if serializer.is_valid():
                        serializer.save()
                        return vcards_id_new
                        #return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
                    else:
                     return CustomeResponse(serializer.errors,status=status.HTTP_201_CREATED)
                
                
                
                
            except:
              pass              
            #----------------------- End--------------------------------------------------#            
            return vcards_id_new
            #---------------------- End---------------------------------------------------#
            
            #--------------- Return the new business card --------------------------------#
            
            #------------------------- End -----------------------------------------------#
    
    