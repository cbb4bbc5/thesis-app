from django import forms

from .models import Note, Tag


class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
    class Meta:
        model = Note
        fields = [
            'name',
            'cr_time',
            'type',
            'description',
            'tags',
        ]
