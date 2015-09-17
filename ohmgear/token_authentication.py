from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import exceptions

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
import datetime
from django.utils.timezone import utc
from ohmgear.functions import custome_response


EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 2)

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        if token.created < timezone.now() - timedelta(hours=EXPIRE_HOURS):
            raise exceptions.AuthenticationFailed('Token has expired')        
        return (token.user, token)
    
    
#class AuthTokenSerializer(serializers.Serializer):
#    username = serializers.CharField()
#    password = serializers.CharField(style={'input_type': 'password'})
#
#    def validate(self, attrs):
#        username = attrs.get('username')
#        password = attrs.get('password')
#
#        if username and password:
#            user = authenticate(username=username, password=password)
#
#            if user:
#                if  user.status != 1:
#                    msg = _('User account is disabled.')
#                    raise exceptions.ValidationError(msg)
#            else:
#                msg = _('Unable to log in with provided credentials.')
#                raise exceptions.ValidationError(msg)
#        else:
#            msg = _('Must include "username" and "password".')
#            raise exceptions.ValidationError(msg)
#
#        attrs['user'] = user
#        return attrs
#    
##---------------------- Token Creation Process ------------------#    
#from rest_framework.authtoken.views import ObtainAuthToken
#class ObtainExpiringAuthToken(ObtainAuthToken):
#    serializer_class = AuthTokenSerializer
#    def post(self, request):
#        serializer = self.serializer_class(data=request.DATA)
#        if serializer.is_valid():
#            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])
#
#            if not created:
#                # update the created time of the token to keep it valid
#                token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
#                token.save()
#
#            return Response(custome_response({'token': token.key},0))
#        return Response(custome_response(serializer.errors,1))
#obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()        