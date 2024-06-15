from django import forms
from dal import autocomplete

from .models import Note, Tag, Connection


class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.order_by('name'),
        widget=autocomplete.ModelSelect2Multiple(url='dashboard:tag-autocomplete'),
        required=False,
    )

    class Meta:
        model = Note
        fields = [
            'name',
            'cr_time',
            'type',
            'description',
            'tags',
        ]

    def save(self):
        instance = forms.ModelForm.save(self)
        instance.tags.clear()
        print(*self.cleaned_data['tags'])
        instance.tags.add(*self.cleaned_data['tags'])
        return instance


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ['note', 'source', 'comment']
        widgets = {'source': autocomplete.ModelSelect2(url='dashboard:note-autocomplete'), }


ConnectionFormSet = forms.inlineformset_factory(
    Note, Connection, form=ConnectionForm, extra=1, can_delete=True,
    fk_name='note',
)

TagFormset = forms.modelformset_factory(
    Tag, fields=['name'], extra=1
)
