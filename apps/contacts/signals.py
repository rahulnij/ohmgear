from django.db.models.signals import post_save
import logging
from .models import ContactMedia
from .tasks import resize_image

logger = logging.getLogger(__name__)


def resize_handler(*args, **kwargs):
    instance = kwargs.get('instance')
    try:
        obj = ContactMedia.objects.get(pk=instance.pk)
    except ContactMedia.DoesNotExist as e:
        logger.critical("Object Does Not Exist: ContactMedia: {}, {}".format(instance.pk, e))
        return

    resize_image.apply_async(obj.img_url, kwargs={'pk': obj.pk})

post_save.connect(resize_handler, sender=ContactMedia)
