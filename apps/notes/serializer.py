from rest_framework import serializers

from apps.notes.models import Notes


class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notes
