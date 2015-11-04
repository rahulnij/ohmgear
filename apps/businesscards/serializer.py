from rest_framework import  serializers
from models import BusinessCard,BusinessCardIdentifier,BusinessCardMedia ,BusinessCardSkillAvailable,BusinessCardAddSkill
from apps.contacts.serializer import ContactsSerializerWithJson
# Serializers define the API representation.
class BusinessCardSerializer(serializers.ModelSerializer):
    #contact_detail1 = serializers.RelatedField(source='contact_detail',read_only= True)    
    bcard_image_frontend = serializers.ImageField(max_length=None, use_url=True,required=False)
    bcard_image_backend = serializers.ImageField(max_length=None, use_url=True,required=False)
    # ------------------- Get the related data like skills identifiers ----------------------#
    contact_detail = ContactsSerializerWithJson(read_only=True)
    #skills = ContactsSerializerWithJson(read_only=True)
    #------------------------ End -----------------------------------------------------------#
    class Meta:
        model = BusinessCard
        fields = (
            'id',
            'name',
            'bcard_type',
            'bcard_image_frontend',
            'bcard_image_backend',
            'is_active',
            'user_id',
            'contact_detail',
        )
  
  
class BusinessCardIdentifierSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = BusinessCardIdentifier
        fields = ('id','identifier','businesscard','status')
          
    def validate(self, attrs):
        #print "dataattaat"
        msg = {}
        value =attrs
        businesscardid =  value['businesscard']
        businesscardid = businesscardid.id
        
        businesscardidentifierdata =     BusinessCardIdentifier.objects.filter(businesscard=businesscardid)
        if not businesscardidentifierdata:
            pass
        else:
            totalbusinesscardrecord =  businesscardidentifierdata.count()
        
            for i in range(totalbusinesscardrecord):
                identifierstatus =  businesscardidentifierdata[i].status
                if(identifierstatus == 1):
                    raise serializers.ValidationError("Businesscard can have 1 identifier only")
        
        return attrs  
    
    
class BusinessCardAddSkillSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BusinessCardAddSkill 
        
class BusinessCardMediaSerializer(serializers.ModelSerializer):
    
    image_url = serializers.ImageField(max_length=None, use_url=True,required=False)
    class Meta:
        model = BusinessCardMedia

class BusinessCardSkillAvailableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BusinessCardSkillAvailable  


