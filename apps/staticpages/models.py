from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField


class StaticPages(models.Model):

    class Meta:
        db_table = 'ohmgear_staticpages'
        
    headline = models.CharField(_("Headline"), max_length=50)
    content = RichTextField()
    page_name = models.CharField(_("Page Name"), unique=True, max_length=20)
    status = models.IntegerField(_("Status"), default=1)
    created_date = models.DateTimeField(
        _("Created Date"), auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(
        _("Updated Date"), auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return '{"id":"%s","content":"%s","page_name":"%s",status":"%s"}' % (
            self.id, self.content, self.page_name, self.status)
