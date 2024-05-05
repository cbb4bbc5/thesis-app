from django.http import HttpResponse
from django.template import loader

from .models import Note, NoteTag, Tag

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
    tags = [nt.tag for nt in note_tags]
    # TODO: take errors into account
    context = {
        'note' : note,
        'tags' : tags,
    }
    # TODO: add display of sources
    return HttpResponse(template.render(context, request))
