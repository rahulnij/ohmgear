from rest_framework import  serializers
from models import BusinessCard,BusinessCardIdentifier,BusinessCardMedia ,BusinessCardSkillAvailable,BusinessCardAddSkill
from apps.contacts.serializer import ContactsSerializerWithJson
# Serializers define the API representation.

  
class BusinessCardIdentifierSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = BusinessCardIdentifier
        fields = ('id','identifier_id','businesscard_id','status')
          
    def validate(self, attrs):
        #print "dataattaat"
        msg = {}
        value =attrs
        businesscardid =  value['businesscard_id']
        businesscardid = businesscardid.id
        
        businesscardidentifierdata =     BusinessCardIdentifier.objects.filter(businesscard_id=businesscardid)
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
        
class BusinessCardAddSkillSerializerReference(serializers.ModelSerializer):
    
    class Meta:
        model = BusinessCardAddSkill
        fields = ('skill_name',)        
        
class BusinessCardMediaSerializer(serializers.ModelSerializer):
    
    img_url = serializers.ImageField(max_length=None, use_url=True,required=True)
    class Meta:
        model = BusinessCardMedia
        fields = ('user_id','businesscard_id','img_url','front_back','position','status')

class BusinessCardSkillAvailableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BusinessCardSkillAvailable  


#----------------- Main Business Card ----------------------------#
class BusinessCardSerializer(serializers.ModelSerializer):

    contact_detail = ContactsSerializerWithJson(read_only=True)
    #identifier_new = serializers.ReadOnlyField(source='*')
    #------------------------ End -----------------------------------------------------------#
    class Meta:
        model = BusinessCard
        fields = (
            'id',
            'name',
            'bcard_type',
            'is_active',
            'status',
            'user_id',
            'contact_detail',
            #'identifier_new',
        )
 
from apps.identifiers.serializer import IdentifierSerializer
from apps.vacationcard.serializer import VacationCardSerializer
class BusinessCardSummarySerializer(serializers.HyperlinkedModelSerializer):
    businesscard_skills = BusinessCardAddSkillSerializerReference(many=True,read_only=True)
    business_identifier = IdentifierSerializer(many=True,read_only=True)
    business_vacation = VacationCardSerializer(many=True,read_only=True)
    media_url = VacationCardSerializer(many=True,read_only=True)
    #------------------------ End -----------------------------------------------------------#
    class Meta:
        model = BusinessCard
        fields = (
            'id',
            'name',
            'businesscard_skills',
            'business_identifier',
            'business_vacation',
        )        
  

