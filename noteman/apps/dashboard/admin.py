from django.contrib import admin
from .models import Note, Connection, Tag, NoteTag

# Register your models here.

admin.site.register(Note)
admin.site.register(Connection)
admin.site.register(Tag)
admin.site.register(NoteTag)
