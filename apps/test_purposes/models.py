from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Ftest(models.Model):

    class Meta:
        db_table = 'ohmgear_ftest'
    name = models.CharField(null=True, max_length=50)
    user = models.ForeignKey(User, related_name='ftestuser')

    def __unicode__(self):
        return'{"id:"%s","name":"%s","user":"%s"}' % (self.id, self.name, self.user)
