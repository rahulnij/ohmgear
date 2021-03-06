import re


def mobile(request):

    device = {}

    ua = request.META.get('HTTP_USER_AGENT', '').lower()

    if ua.find("iphone") > 0:
        #device['iphone'] = "iphone" + re.search("iphone os (\d)", ua).groups(0)[0]
        device['iphone'] = "iphone"

    if ua.find("ipad") > 0:
        device['ipad'] = "ipad"

    if ua.find("android") > 0:
        #device['android'] = "android" + re.search("android (\d\.\d)", ua).groups(0)[0].translate(None, '.')
        device['android'] = "android"

    # spits out device names for CSS targeting, to be applied to <html> or <body>.
    #device['classes'] = " ".join(v for (k,v) in device.items())

    return device


class MobileDetectionMiddleware(object):
    """
    Useful middleware to detect if the user is
    on a mobile device.
    """

    def process_request(self, request):
        device = mobile(request)
        request.device = device
