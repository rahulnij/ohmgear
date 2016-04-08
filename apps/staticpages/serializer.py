from rest_framework import serializers

from models import StaticPages


class StaticPagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaticPages
