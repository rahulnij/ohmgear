from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import Notes
from serializer import NotesSerializer
from ohmgear.functions import CustomeResponse
from rest_framework.decorators import api_view
import rest_framework.status as status

# Create your views here.
class NotesViewSet(viewsets.ModelViewSet):
    #queryset = Notes.objects.all()
    #serializer_class = NotesSerializer
    queryset = Notes.objects.select_related().all()
    serializer_class = NotesSerializer
    #--------------Method: GET-----------------------------#       
    def list(self,request):
         return CustomeResponse({'msg':'GET method not allowed'},status=status.HTTP_405_METHOD_NOT_ALLOWED,validate_errors=1)
 
    #--------------Method: GET retrieve single record-----------------------------#
    def retrieve(self, request,pk=None):
        queryset = self.queryset
        notes = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(notes,context={'request': request})
        
        return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
    
    #--------------Method: POST create new Note -----------------------------#
    def create(self, request,call_from_function=None):
         
         serializer =  NotesSerializer(data=request.DATA,context={'request': request})
         if serializer.is_valid():
            note_id=serializer.save() 
            if not call_from_function:
             return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
            else:
             return serializer.data   
         else:
           if not call_from_function:  
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
           else:
             return serializer.errors   
    
        
    def update(self, request, pk=None):
         try:
           messages = Notes.objects.get(id=pk)
         except:
           return CustomeResponse({'msg':'record not found'},status=status.HTTP_404_NOT_FOUND,validate_errors=1)
         serializer =  NotesSerializer(messages,data=request.DATA,partial=True,context={'request': request})
         if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
         else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)

    
    def partial_update(self, request, pk=None):
        pass

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_200_OK) 

