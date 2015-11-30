from rest_framework import serializers
from models import Folder
class FolderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Folder
		fields = ('id','foldername','businesscard_id')
	
	
	def validate_foldername(self, value):
		print len(value) 
		if len(value) > 30:
			raise serializers.ValidationError("Folder name length not more than 2")

		return value
	
