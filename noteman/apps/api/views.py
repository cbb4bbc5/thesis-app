from apps.dashboard.models import Note, NoteTag, Tag, Connection
from rest_framework import viewsets

from .serializers import NoteSerializer, NoteTagSerializer, TagSerializer, ConnectionSerializer
from .filters import NoteFilter


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.order_by('-cr_time')
    serializer_class = NoteSerializer
    filterset_class = NoteFilter
    ordering_fields = ['cr_time']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filterset_fields = {
        'name': ['exact', 'icontains', 'contains'],
    }


class NoteTagViewSet(viewsets.ModelViewSet):
    queryset = NoteTag.objects.all()
    serializer_class = NoteTagSerializer
    filterset_fields = ['note', 'tag']


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    filterset_fields = ['note', 'source']
