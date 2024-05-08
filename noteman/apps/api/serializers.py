from rest_framework import serializers

from apps.dashboard.models import Note, Tag, NoteTag, Connection


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        # per documentation, it is recommended to explicitly specify fields
        # even though by default all of them are returned
        fields = [
            'id',
            'name',
            'cr_time',
            'type',
            'description',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]
