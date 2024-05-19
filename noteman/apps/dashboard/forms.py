from django import forms

from .models import Note, Tag, Connection


class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.order_by('name'),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = Note
        fields = [
            'name',
            'cr_time',
            'type',
            'description',
        ]
    def save(self):
        # https://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
        # creating custom save function was enough to savee tag info however I do not
        # fully understand how it works, as I think manytomany should have been saved
        # without having to modify save function
        instance = forms.ModelForm.save(self)
        instance.tags.clear()
        instance.tags.add(*self.cleaned_data['tags'])
        # instance.references.clear()
        # instance.references.add(*self.cleaned_data['references'])
        return instance


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ['note', 'source', 'comment']


ConnectionFormSet = forms.inlineformset_factory(
    Note, Connection, form=ConnectionForm, extra=1, can_delete=True,
    fk_name='note',
)
