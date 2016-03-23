from django.contrib.gis.db import models



class UserLocation(models.Model):
    class Meta:
        unique_together = ('user_id', 'region')
        db_table = 'ohmgear_user_location'

    user_id = models.IntegerField()
    region  = models.CharField(max_length=4)
    
    geom = models.PointField(srid=4326)
    objects = models.GeoManager()
    updated_date = models.DateTimeField(auto_now=True);


    def __unicode__(self):
    	return '{"user_id":%r,"region":%r, "lon":%r, "lat":%r, "updated_date":%r}' % (self.user_id, self.region, self.geom.x, self.geom.y, self.updated_date)
