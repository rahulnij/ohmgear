
# django imports
from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework import viewsets

# third party imports
from ohmgear.functions import CustomeResponse
import rest_framework.status as status
import datetime
import random

# application imports
from models import Identifier, LockIdentifier
from serializer import IdentifierSerializer, LockIdentifierSerializer, BusinessIdentifierSerializer
from functions import CreateSystemIdentifier


# Create your views here.


class IdentifierViewSet(viewsets.ModelViewSet):
    queryset = Identifier.objects.select_related().all()
    serializer_class = IdentifierSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, **kwargs):
        if request.method == 'GET':

            identifier = self.request.query_params.get('identifier', None)

            # check whether idnetifier is exist or not if not give suggested identifier
            identifierdata = Identifier.objects.filter(
                identifier=identifier).values()

            # Get all identifiers of the user
            user = self.request.query_params.get('user', None)
            userdata = Identifier.objects.select_related(
                'businesscard_identifiers').filter(user=user).order_by('-id')

            serializer = BusinessIdentifierSerializer(userdata, many=True)

            if userdata:
                return CustomeResponse(serializer.data, status=status.HTTP_201_CREATED)
            else:
                if identifier is None:
                    return CustomeResponse({'msg': 'user id is not exist'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
                if not identifierdata and identifier is not None:
                    return CustomeResponse({'msg': 'Identifier available'}, status=status.HTTP_200_OK)

                else:
                    list = []
                    for i in range(5):
                        identifiersuggestion = ''.join(
                            random.choice('0123456789') for i in range(2))
                        newidentifier = identifier + identifiersuggestion
                        matchidentifier = Identifier.objects.filter(
                            identifier=newidentifier).values()
                        if not matchidentifier:
                            list.append(newidentifier)
                    return CustomeResponse({"msg": list}, status=status.HTTP_200_OK, validate_errors=True)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        identifier = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(
            identifier, context={'request': request})

        return CustomeResponse(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        data = request.data.copy()
        data['user'] = request.user.id
        data['identifierlastdate'] = str(
            (datetime.date.today() + datetime.timedelta(3 * 365 / 12)).isoformat())

        if request.POST.get('identifiertype') == '1':
            pass

        else:
            pass

        serializer = IdentifierSerializer(
            data=data, context={'request': request, 'msg': 'not exist'})

        if serializer.is_valid():
            serializer.save()
            remove_lock_data = LockIdentifier.objects.filter(
                identifier=request.POST.get('identifier'))
            if remove_lock_data:
                remove_lock_data.delete()
            return CustomeResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)

    @list_route(methods=['post'],)
    def refreshidentifier(self, request):

        try:
            user_id = request.user
        except:
            user_id = None

        if user_id:
            getidentifier = CreateSystemIdentifier()

            if getidentifier:
                return CustomeResponse({'identifier': getidentifier}, status=status.HTTP_200_OK)
            else:
                return CustomeResponse({'msg': 'Identifier Not exist'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        else:
            return CustomeResponse({'msg': 'Invalid User'}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)


    @list_route(methods=['post'],)
    def lockidentifier(self, request):
        print request.POST.get('identifier')
        try:
            user_id = request.user
        except:
            user_id = None
        data = {}
        data['user'] = request.user.id
        data['identifier'] = request.POST.get('identifier')

        serializer = LockIdentifierSerializer(
            data=data, context={'request': request, 'msg': 'not exist'})

        if serializer.is_valid():
            identifier_exist = Identifier.objects.filter(
                identifier=data['identifier'])
            identifier_lock_exist = LockIdentifier.objects.filter(
                identifier=data['identifier'])
            if identifier_exist or identifier_lock_exist:
                return CustomeResponse({'msg': 'Identifier is already locked'})
            else:
                serializer.save()
                return CustomeResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse({'msg': serializer.errors}, validate_errors=1)
