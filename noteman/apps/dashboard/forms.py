from django import forms

from .models import Note, Tag, Connection


class NoteForm(forms.ModelForm):
    # https://stackoverflow.com/questions/56077861/how-to-make-choicefield-not-required
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
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
        # creating custom save function was enough to save tag info however I do not
        # fully understand how it works, as I think manytomany should have been saved
        # without having to modify save function
        instance = forms.ModelForm.save(self)
        instance.tags.clear()
        print(*self.cleaned_data['tags'])
        instance.tags.add(*self.cleaned_data['tags'])
        return instance


class ConnectionForm(forms.ModelForm):
    tester = True
    if tester:
        source = forms.ModelChoiceField(queryset=Note.objects.all())
    else:
        source = forms.ModelChoiceField(
            queryset=Note.objects.all(),
            widget=forms.TextInput(attrs={'class': 'autocomplete'}),
            empty_label=None,
        )
    class Meta:
        model = Connection
        fields = ['note', 'source', 'comment']


ConnectionFormSet = forms.inlineformset_factory(
    Note, Connection, form=ConnectionForm, extra=1, can_delete=True,
    fk_name='note',
)

TagFormset = forms.modelformset_factory(
    Tag, fields=['name'], extra=1
)
