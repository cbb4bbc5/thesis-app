from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, get_object_or_404
from dal import autocomplete

from .forms import NoteForm, ConnectionFormSet, TagFormset
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
    # predecessors = [connection.source for connection in connections]
    # TODO: take errors into account
    context = {
        'note': note,
        'tags': tags,
        'connections': connections,
    }
    return HttpResponse(template.render(context, request))


def all_tags(request):
    template = loader.get_template('dashboard/all_tags.html')
    tags = Tag.objects.order_by('name')
    tag_formset = TagFormset(queryset=Tag.objects.none())
    if request.method == "POST":
        tag_formset = TagFormset(request.POST)
        if tag_formset.is_valid():
            tag_formset.save()
            return redirect('dashboard:all_tags')
    context = {
        'tags': tags,
        'tag_formset': tag_formset,
    }
    return HttpResponse(template.render(context, request))


class NoteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Note.objects.order_by('-cr_time')

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class TagAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.order_by('name')

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


def add_note(request, note_id=None):
    template = loader.get_template('dashboard/add_note.html')
    context = {}
    notes = Note.objects.all()
    to_edit = None
    if note_id:
        to_edit = get_object_or_404(Note, pk=note_id)
    if request.method == "POST":
        note_form = NoteForm(request.POST)
        connection_formset = ConnectionFormSet(request.POST)
        if to_edit:
            note_form = NoteForm(request.POST, instance=to_edit)
            connection_formset = ConnectionFormSet(request.POST, instance=to_edit)
        if note_form.is_valid() and connection_formset.is_valid():
            note = note_form.save()
            connections = connection_formset.save(commit=False)
            for connection in connections:
                connection.note = note
                connection.save()
            for connection in connection_formset.deleted_objects:
                connection.delete()
            connection_formset.save_m2m()
            if to_edit:
                return redirect('dashboard:all_notes')
            return redirect('dashboard:add_note')
    else:
        note_form = NoteForm()
        connection_formset = ConnectionFormSet()
        if to_edit:
            note_form = NoteForm(instance=to_edit)
            connection_formset = ConnectionFormSet(instance=to_edit)

    context = {
        'note_form': note_form,
        'connection_formset': connection_formset,
        'notes': notes,
    }
    return HttpResponse(template.render(context, request))
