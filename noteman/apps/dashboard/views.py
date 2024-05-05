from django.http import HttpResponse
from django.template import loader

from .models import Note, NoteTag, Tag, Connection

def index(request):
    template = loader.get_template('common/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def all_notes(request):
    template = loader.get_template('dashboard/all_notes.html')
    notes = Note.objects.all()
    context = {
        'notes' : notes,
    }
    return HttpResponse(template.render(context, request))

def note_detail(request, note_id):
    template = loader.get_template('dashboard/note.html')
    note = Note.objects.get(pk=note_id)
    note_tags = NoteTag.objects.filter(note__id=note_id)
    # TODO: maybe rewrite getting tags in some more elegant way? like using something similar to values
    # https://stackoverflow.com/questions/7503241/how-to-obtain-a-queryset-of-all-rows-with-specific-fields-for-each-one-of-them
    # found this but not what I am looking for
    # also this seems more important: https://docs.djangoproject.com/en/5.0/ref/models/querysets/
    tags = [nt.tag for nt in note_tags]
    connections = Connection.objects.filter(note__id=note_id)
    predecessors = [connection.source for connection in connections]
    # TODO: take errors into account
    context = {
        'note' : note,
        'tags' : tags,
        'sources' : predecessors,
    }
    return HttpResponse(template.render(context, request))
