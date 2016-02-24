from rest_framework import serializers
from models import Folder,FolderContact,MatchContact

class FolderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Folder
		fields = ('id','foldername','businesscard_id')
	
	
	def validate_foldername(self, value):
		if len(value) > 30:
			raise serializers.ValidationError("Folder name length not more than 2")

		return value
            
            
class FolderContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = FolderContact
		fields = ('id','user_id','folder_id','contact_id') 
                
                
class MatchContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = MatchContact
		fields = ('id','user_id','folder_contact_id','businesscard_id')                
	
