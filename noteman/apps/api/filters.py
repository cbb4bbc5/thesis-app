import django_filters

from apps.dashboard.models import Note, Tag


class NoteFilter(django_filters.FilterSet):
    class Meta:
        model = Note
        fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'contains'],
            'cr_time': ['gte', 'lte'],
            'type': ['exact'],
        }
