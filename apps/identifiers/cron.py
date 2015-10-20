#from models import Identifier
from apps.identifiers.models import Identifier

def my_scheduled_job():
    queryset = Identifier.objects.select_related().all()
    print "cronsddd"
    print queryset
    