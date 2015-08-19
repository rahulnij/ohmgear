from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
# We are using this class for custom user login as login functionality
class UsersModelFrontEnd(ModelBackend):
    def authenticate_frontend(self, username=None, password=None):
        
        try:
            user = get_user_model().objects.get(email=username,user_type__in=[2,3])
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:            
            return None
    
    