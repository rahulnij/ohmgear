# Import Python Modules
from collections import OrderedDict
# Third Party Imports
from django.conf.urls import url, include
from models import Group, GroupContacts
from rest_framework import routers, serializers, viewsets


class GroupSerializer(serializers.ModelSerializer):
    attached_group_contacts = serializers.IntegerField(
        source='group_data.count', read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'group_name', 'attached_group_contacts')


class GroupContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupContacts
