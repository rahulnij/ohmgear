#from models import Identifier
from apps.identifiers.models import Identifier
from functions import CreateSystemIdentifier

import datetime

def updateidentifierstatus():
    currentdate = datetime.date.today()
    print "currentdate"
    print currentdate
    
    #queryset = Identifier.objects.select_related().all()
    
    #------------First time user will get premium identifier for 3 months after that premium identifier will replace by sytem identifier----#
    getfreeexpiredpremiumidentifier = Identifier.objects.filter(identifierlastdate = currentdate, paymentstatus =0,status=1,identifiertype=2,totalmonths=3).values()
    if getfreeexpiredpremiumidentifier:
        #-----------premium identifier replaced by system-------#
        totalrecord =  getfreeexpiredpremiumidentifier.count()
        
        for i in range(totalrecord):
            Identifier.objects.filter(id=getfreeexpiredpremiumidentifier[i]['id']).update(identifier= CreateSystemIdentifier(),identifiertype = 1,identifierlastdate = str((datetime.date.today() + datetime.timedelta(3*365/12)).isoformat()) )
            #print "run api for systematic identifier"
        
    
    
    #------------------ After 3 months of premium identifier system identifier will be given for  3 months  and after that it will get expire and identifier status will be 0-------#
    getfreeexpiredsystemidentifier = Identifier.objects.filter(identifierlastdate = currentdate, paymentstatus = 0,status = 1,identifiertype = 1).values()
    if getfreeexpiredsystemidentifier:
        totalfreeexpiredsystemidentifierrecord =  getfreeexpiredsystemidentifier.count()
        
        for i in range(totalfreeexpiredsystemidentifierrecord):
            Identifier.objects.filter(id=getfreeexpiredsystemidentifier[i]['id']).update(status= 0 )
        
            #print "update query make status 0 "
    
        
    #------------------premium identifier user have paid for premium but now expired  -------#
    getpaidexpiredpremiumidentifier = Identifier.objects.filter(identifierlastdate = currentdate, paymentstatus =1,status=1,identifiertype=2).values()    
    if getpaidexpiredpremiumidentifier:
       totalpaidexpiredpremiumidentifierrecord =  getpaidexpiredpremiumidentifier.count()
       
       for i in range(totalpaidexpiredpremiumidentifierrecord):
            Identifier.objects.filter(id=getpaidexpiredpremiumidentifier[i]['id']).update(status= 0,paymentstatus =0)
            #print "update query make status 0 and payement status 0 for premium identifier"  
    
    
    #------------------System identifier user have paid for system but now expired  -------#    
    getpaidexpiredsystemidentifier = Identifier.objects.filter(identifierlastdate = currentdate, paymentstatus =1,status=1,identifiertype=1).values()    
    if getpaidexpiredsystemidentifier:
        totalpaidexpiredsystemidentifier = getpaidexpiredsystemidentifier.count()
        
        for i in range(totalpaidexpiredsystemidentifier):
            Identifier.objects.filter(id = getpaidexpiredsystemidentifier[i]['id']).update(status =0 ,paymentstatus = 0)
            #print "update query make status 0 and payement status 0 for system identifier"  
    
    
    
    