from django.db import models

# Create your models here.


class UserLocation(models.Model):
    class Meta:
        unique_together = ('user_id', 'region')
        db_table = 'ohmgear_user_location'

    user_id = models.IntegerField()
    region  = models.CharField(max_length=4)
    lon = models.FloatField()
    lat = models.FloatField()
    updatedDate = models.DateTimeField(auto_now=True);


    def __unicode__(self):
    	return '{"user_id":%r,"region":%r, "lon":%r, "lat":%r, "updatedDate":%r}' % (self.user_id, self.region, self.lon, self.lat, self.updatedDate)
