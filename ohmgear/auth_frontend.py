from django.contrib.auth import get_user_model
# We are using this class for custom user login as login functionality


def authenticate_frontend(username=None, password=None):

    try:
        user = get_user_model().objects.get(
            email=username, user_type__in=[2, 3], status=1)
        if user.check_password(password):
            return user
    except:
        return None
