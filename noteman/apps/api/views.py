from rest_framework import viewsets

from apps.dashboard.models import Note, Tag
from .serializers import NoteSerializer, TagSerializer

# https://www.django-rest-framework.org/api-guide/generic-views/#generic-views

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.order_by('-cr_time')
    serializer_class = NoteSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
