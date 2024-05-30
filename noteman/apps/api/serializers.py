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
            'tags',
            'references',
        ]
        read_only_fields = [
            'id',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
        ]
        read_only_fields = [
            'id',
        ]


class NoteTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteTag
        fields = [
            'id',
            'note',
            'tag',
        ]
        read_only_fields = [
            'id',
        ]


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = [
            'id',
            'note',
            'source',
        ]
        read_only_fields = [
            'id',
        ]
