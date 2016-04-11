from PIL import Image
from .celery import app
from .models import ContactMedia
from os import path
import logging

logger = logging.getLogger(__name__)


@app.task
def resize_image(image_path, dim_x, landscape=True):
    with open(image_path, 'r') as orig:
        im = Image.open(orig, mode='r')
        new_y = (float(dim_x) * float(im.height)) / float(im.width)
        new_im = im.resize((dim_x, int(new_y)))
        img_path, img_name = path.split(image_path)
        _, img_ext = img_name.split('.')
        new_img_path = path.join(img_path, img_name + '_resized' + img_ext)
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
