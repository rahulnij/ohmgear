import rest_framework.status as status

# Create your model here.
from apps.test_purposes.models import Ftest
from apps.users.serializer import UserSerializer
# Create your serializer here here.
from rest_framework import serializers
#------------- Serializer to show related data in one leverl ---------------_#


class FtestSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Ftest
        fields = (
            'id',
            'name',
            'first_name',
            'email',
        )
# Create your view here.
from rest_framework import viewsets


class FtestViewSet(viewsets.ModelViewSet):
    queryset = Ftest.objects.all()
    serializer_class = FtestSerializer

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset
