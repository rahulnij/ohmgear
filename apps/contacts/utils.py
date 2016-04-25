from .models import ContactMedia
from common.image_lib import resize_image, MAX_WIDTH
from logging import getLogger
logger = getLogger(__name__)


def resize_contact_media_image(**kwargs):
    try:
        contact_media = ContactMedia.objects.get(kwargs.get('pk'))
    except ContactMedia.DoesNotExist as e:
        logger.error("Caught DoesNotExist exception for ContactMedia with prmary key {}, in {}".format(
            kwargs.get('pk'), __file__)
        )
        # TODO: Notify Sentry
        return
    new_img_path = resize_image(contact_media.img_url, MAX_WIDTH)
    contact_media.img_url = new_img_path
    try:
        contact_media.save()
    except Exception as e:
        logger.critical("Caught Exception {} in {}".format(e, __file__))
        # TODO: Notify Sentry