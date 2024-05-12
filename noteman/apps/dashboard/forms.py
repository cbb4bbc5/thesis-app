from django import forms

from .models import Note, NoteTag


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'name',
            'cr_time',
            'type',
            'description',
        ]


class NoteTagForm(forms.ModelForm):
    class Meta:
        model = NoteTag
        fields = [
            'note',
            'tag',
        ]
