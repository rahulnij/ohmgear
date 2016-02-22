from django.shortcuts import render
from rest_framework import routers,serializers,viewsets
from models import Group,GroupContacts
from serializer import GroupSerializer,GroupContactsSerializer
from ohmgear.functions import CustomeResponse
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
import rest_framework.status as status
from rest_framework.decorators import detail_route, list_route
# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
    
    queryset = Group.objects.all()
    serializer_class =  GroupSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,) 

#----------Method: Get---------------------------#
    def list(self,request):
        group_data = self.queryset.filter(user_id=request.user)
        try:
            serializer = self.serializer_class(group_data,many=True)
        except:
            return CustomeResponse({'msg':'server error please try after some time'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        if serializer.data:
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg':'Data not found for this user'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
 #------------------Method: insert group--------------#       
    def create(self,request):
        try:
            user_id = request.user
        except:
            user_id =''
        data ={}
        data   =request.DATA.copy()
        data['user_id'] = request.user.id
    
        serializer = self.serializer_class(data=data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:    
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
#-----------------Method: Update group------------#        
    def update(self,request,pk=None):
        try:
            user_id = request.user
        except:
            user_id = request.user.id
        try:
            group_data = self.queryset.filter(user_id=request.user.id,id=pk)
        except:
            return CustomeResponse({'msg':'Data not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
         
        if group_data:
            group_data.update(group_name=request.data['group_name'])
            return CustomeResponse({'msg':'Data is updated'},status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg':'Data cannot be updated'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
            
#-------------Method : Delete group----------------#
    @list_route(methods=['post'],)       
    def deletegroups(self,request):
         
        try:
            user_id = request.user.id
        except:
            user_id = ''
        
        try:
            group_id = request.data['group_id']
        except:
            return CustomeResponse({'msg':'group_id not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        try:
            group_data =    self.queryset.filter(user_id=user_id,id__in=group_id)
        except:
            return CustomeResponse({'msg':'group not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        if group_data:
            group_data.delete()
            return CustomeResponse({'msg':'group deleted successfully'},status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg':'group cannot be deleted'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
        
class GroupContactsViewSet(viewsets.ModelViewSet):
    queryset = GroupContacts.objects.all()
    serializer_class = GroupContactsSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permisssion_classes    = IsAuthenticated
    
    
    def list(self,request):
        group_data = self.queryset.filter(user_id=request.user)
        try:
            serializer = self.serializer_class(group_data,many=True)
        except:
            return CustomeResponse({'msg':'server error please try after some time'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        if serializer.data:
            return CustomeResponse(serializer.data,status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg':'Data not found for this user'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
#        return CustomeResponse({'msg':'Get method bnot allowed'})
    
    def create(self,request):
        
        try:
            user_id = request.user.id
        except:
            user_id = ''
            
        try:
            group_contacts = request.data['group_contacts']
        except:
            return CustomeResponse({'msg':'group contacts not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        tempContainer = []
        for contacts in group_contacts:
             data = {}
             data['folder_contact_id'] = contacts['folder_contact_id']
             data['group_id']          = contacts['group_id']
             data['user_id']           = user_id
             group_contact_data_exist = self.queryset.filter(user_id=request.user,folder_contact_id=data['folder_contact_id'],group_id=data['group_id'])
             if group_contact_data_exist:
                 return CustomeResponse({'msg':'contact is already added with this user'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
                 
             tempContainer.append(data)
             
        serializer = self.serializer_class(data=tempContainer,many=True,context={'contact_data': 1})
        if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
        
    @list_route(methods=['post'],)    
    def delete(self,request):
        try :
            user_id =request.user.id
        except:
            user_id = ''
            
        try:
            group_contact_id = request.data['group_contact_id']
            print group_contact_id
        except:  
            return CustomeResponse({'msg':'group contact id not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
         
        try:
             group_contact_data = self.queryset.filter(user_id=user_id,id__in=group_contact_id)
        
        except:
            return CustomeResponse({'msg':'group contact data not found'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
             
        
        if group_contact_data:
            group_contact_data.delete()
            return CustomeResponse({'msg':'contact deleted successfully'},status=status.HTTP_200_OK)
        else:
            return CustomeResponse({'msg':'contact cannot be deleted for this user'},status=status.HTTP_400_BAD_REQUEST,validate_errors=1)
        
    

