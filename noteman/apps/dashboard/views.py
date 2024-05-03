from django.http import HttpResponse
from django.template import loader

from .models import Note

def index(request):
    template = loader.get_template('common/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def note_detail(request, note_id):
    template = loader.get_template('dashboard/note.html')
    note = Note.objects.get(pk=note_id)
    # TODO: take errors into account
    context = {
        'note' : note,
    }
    # TODO: add display of tags
    # TODO: add display of sources
    return HttpResponse(template.render(context, request))
