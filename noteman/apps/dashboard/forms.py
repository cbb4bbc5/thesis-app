from django import forms

from .models import Note, Tag


class NoteForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=forms.CheckboxSelectMultiple)
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
        return instance
