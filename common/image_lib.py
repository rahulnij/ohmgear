from PIL import Image
# from apps.celery import celery_app as app
# from apps.contacts.models import ContactMedia
from os import path
import logging

logger = logging.getLogger(__name__)

MAX_WIDTH = 1920
THUMB_WIDTH = 50


# @app.task
def resize_image(image_path, dim_x, append_str='_resized', **kwargs):
    '''
    resize any image while maintaining aspect ratio
    '''
    with open(image_path, 'r') as orig:
        im = Image.open(orig, mode='r')
        new_y = (float(dim_x) * float(im.height)) / float(im.width)
        new_im = im.resize((dim_x, int(new_y)))
        img_path, img_name = path.split(image_path)
        file_name, img_ext = img_name.split('.')
        new_img_path = path.join(img_path, file_name + append_str + '.' + img_ext)
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
        

def image_dimensions(image_path):
    with open(image_path) as f:
        im = Image.open(f, 'r')
        height = im.height
        width = im.width
    return (width, height)


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
    thumb_img_path = resize_image(obj.img_url, THUMB_WIDTH, append_str='_thumb')
    obj.img_url = thumb_img_path
    try:
        obj.save()
    except Exception as e:
        logger.critical("Caught Exception {} in {}".format(e, __file__))
        # TODO -- notify Sentry

