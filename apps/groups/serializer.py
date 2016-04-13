# Import Python Modules
from collections import OrderedDict
# Third Party Imports
from django.conf.urls import url, include
from models import Group, GroupContacts, GroupMedia
from rest_framework import routers, serializers, viewsets
from django.conf import settings

class GroupSerializer(serializers.ModelSerializer):
    attached_group_contacts = serializers.IntegerField(
        source='group_data.count', read_only=True)
    group_media = serializers.SerializerMethodField(
        'group_image')

    def group_image(self, obj):
        media = GroupMedia.objects.filter(
            group_id=obj.id, status=1)
        print "media"
        print media
        data = []

        for item in media:
            data.append({"img_url": str(settings.DOMAIN_NAME) +
                         str(settings.MEDIA_URL) +
                         str(item.img_url)})
        return data

    class Meta:
        model = Group
        fields = (
            'id',
            'group_name',
            'description',
            'attached_group_contacts',
            'group_media')


class GroupContactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupContacts


class GroupMediaSerializer(serializers.ModelSerializer):

    img_url = serializers.ImageField(
        max_length=None, use_url=True, required=True)

    class Meta:
        model = GroupMedia
        fields = ('user_id', 'group_id', 'img_url', 'status')
