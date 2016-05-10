from django.conf import settings


def get_contact_media(media=None):
    data_media = []

    for item in media:
        data_media.append({"img_url": str(settings.DOMAIN_NAME) +
                           str(settings.MEDIA_URL) +
                           str(item.img_url), "front_back": item.front_back})
    return data_media
