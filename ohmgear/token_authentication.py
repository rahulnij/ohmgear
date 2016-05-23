from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import exceptions

# from rest_framework.authtoken.models import Token

from django.utils.translation import ugettext_lazy as _

#
EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 72)


class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = self.get_model().objects.get(key=key)
        except self.get_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
        # check user status if user status 0 that means user still did not
        # verified his account
        if token.user.status == 0:
            if token.created < timezone.now() - timedelta(hours=EXPIRE_HOURS):
                raise exceptions.AuthenticationFailed('not verified user')
        return (token.user, token)


# class AuthTokenSerializer(serializers.Serializer):
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
# class ObtainExpiringAuthToken(ObtainAuthToken):
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
