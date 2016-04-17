from PIL import Image
from .celery import app
from .models import ContactMedia
from os import path
import logging

logger = logging.getLogger(__name__)

MAX_WIDTH = 1920
THUMB_WIDTH = 50


@app.task
def resize_image(image_path, dim_x, append_str='_resized', **kwargs):
    '''
    resize any image while maintaining aspect ratio
    '''
    with open(image_path, 'r') as orig:
        im = Image.open(orig, mode='r')
        new_y = (float(dim_x) * float(im.height)) / float(im.width)
        new_im = im.resize((dim_x, int(new_y)))
        img_path, img_name = path.split(image_path)
        _, img_ext = img_name.split('.')
        new_img_path = path.join(img_path, img_name + append_str + img_ext)
        try:
            f = open(new_img_path, 'w')
        except IOError as e:
            logger.critical("Caught IOError in {}, {}".format(__file__, e))
            return 
        try:
            new_im.save(f)
        except IOError as e:
            logger.critical("Caught IOError in {}, {}".format(__file__, e))
            return
        f.close()
        return new_img_path
        

@app.task
def image_properties(image_path, img_id):
    contact_media = ContactMedia.objects.get(pk=img_id)
    with open(image_path) as f:
        im = Image.open(f, 'r')
        contact_media.height = im.height
        contact_media.width = im.width
        if im.height > im.width:
            contact_media.position = 1
        else:
            contact_media.position = 2


@app.task
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


@app.task
def thumbnail(cls, **kwargs):
    """
    given any image, resize to 50 * n pixles
    so that aspect ratio is maintained
    """
    try:
        obj = cls.objects.get(kwargs.get('pk'))
    except cls.DoesNotExist as e:
        logger.error("Caught DoesNotExist exception for {} with prmary key {}, in {}".format(
            cls, kwargs.get('pk'), __file__)
        )
        # TODO: Notify Sentry
        return
    thumb_img_path = resize_image(obj.image_path, THUMB_WIDTH, append_str='_thumb')
    obj.img_url = thumb_img_path
    try:
        obj.save()
    except Exception as e:
        logger.critical("Caught Exception {} in {}".format(e, __file__))
        # TODO -- notify Sentry

