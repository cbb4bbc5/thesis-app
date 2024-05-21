from django.http import HttpResponse
from django.template import loader

from .forms import NoteForm, ConnectionFormSet
from .models import Connection, Note, NoteTag, Tag


def index(request):
    template = loader.get_template('common/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def all_notes(request):
    template = loader.get_template('dashboard/all_notes.html')
    notes = Note.objects.order_by('-cr_time')
    tags = Tag.objects.order_by('name')
    context = {
        'notes': notes,
        'tags': tags,
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
        'note': note,
        'tags': tags,
        'sources': predecessors,
    }
    return HttpResponse(template.render(context, request))


def all_tags(request):
    template = loader.get_template('dashboard/all_tags.html')
    tags = Tag.objects.order_by('name')
    context = {
        'tags': tags,
    }
    return HttpResponse(template.render(context, request))


def add_note(request):
    template = loader.get_template('dashboard/add_note.html')
    context = {}
    note_form = NoteForm()
    connection_formset = ConnectionFormSet()
    # TODO: combine note form and tag form into one
    if request.POST:
        note_form = NoteForm(request.POST)
        connection_formset = ConnectionFormSet(request.POST)
        if note_form.is_valid() and connection_formset.is_valid():
            note = note_form.save()
            connections = connection_formset.save(commit=False)
            for connection in connections:
                connection.note = note
                connection.save()
    context['note_form'] = note_form
    context['connection_formset'] = connection_formset
    return HttpResponse(template.render(context, request))
