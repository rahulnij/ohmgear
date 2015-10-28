from django.conf import settings
#------------------ Return token if does not exit then create -------------------#  
from models import BusinessCard
from apps.contacts.models import Contacts
from apps.notes.models import Notes

def createDuplicateBusinessCard(bcard_id=None):
    
    if bcard_id:
            #-------------------- Duplicate Business card row ---------------------------# 
            bcards = BusinessCard.objects.select_related("contact_detail").get(id=bcard_id)
            bcards.id = None
            bcards.save()
            bcards_id_new = bcards.id
            contact_id  = bcards.contact_detail.id
            #---------------------- End---------------------------------------------------#
            
            #--------------------- Duplicate Contact row ------------------------#
            try:
                contact = Contacts.objects.get(businesscard_id=bcard_id)
                contact.id = None
                contact.businesscard_id = BusinessCard.objects.get(id=bcards_id_new)
                contact.save()
                contact_id_new =contact.id
            except:
              pass              
            #----------------------- End--------------------------------------------------#
            #--------------------- Duplicate Notes ---------------------------------------#
            try:
                note = Notes.objects.get(contact_id=contact_id,bcard_side_no=1)
                note.contact_id = Contacts.objects.get(id=contact_id_new)   
                note.id = None 
                note.save()
            except:
                pass
            
            try:
                note = Notes.objects.get(contact_id=contact_id,bcard_side_no=2)
                note.contact_id = Contacts.objects.get(id=contact_id_new)   
                note.id = None 
                note.save()
            except:
                pass    
            
            return bcards_id_new
            #---------------------- End---------------------------------------------------#
            
            #--------------- Return the new business card --------------------------------#
            
            #------------------------- End -----------------------------------------------#
            
            
  
    
    