from apps.dashboard.models import Note, NoteTag, Tag
from rest_framework import viewsets

from .serializers import NoteSerializer, NoteTagSerializer, TagSerializer

# https://www.django-rest-framework.org/api-guide/generic-views/#generic-views
# TODO: remove branding? https://stackoverflow.com/questions/51393960/django-rest-browsable-api-template-change

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.order_by('-cr_time')
    serializer_class = NoteSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class NoteTagViewSet(viewsets.ModelViewSet):
    queryset = NoteTag.objects.all()
    serializer_class = NoteTagSerializer
