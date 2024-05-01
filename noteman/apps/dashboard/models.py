from datetime import datetime as dt

from django.db import models
from django.db.models.functions import Now


class Note(models.Model):
    name = models.CharField(max_length=200)
    # db_default or default
    # https://stackoverflow.com/questions/77665050/what-does-the-new-field-db-default-of-django-5-imply-should-we-use-it-by-def
    cr_time = models.DateTimeField(default=Now)
    # TODO: use choices for type_id, like here
    # https://stackoverflow.com/questions/48040008/django-restrict-data-that-can-be-given-to-model-field
    type = models.IntegerField()
    description = models.CharField(max_length=200)

"""Example code (copy for tests)
import apps.dashboard.models

n1 = apps.dashboard.models.Note.objects.get_or_create(name='First note', type=1, description='this is a first note')[0]
n2 = apps.dashboard.models.Note.objects.get_or_create(name='Second note', type=1, description='this is a second note')[0]
n3 = apps.dashboard.models.Note.objects.get_or_create(name='Third note', type=1, description='this is a third note')[0]

t1 = apps.dashboard.models.Tag.objects.get_or_create(name='red')[0]
t2 = apps.dashboard.models.Tag.objects.get_or_create(name='blue')[0]
t3 = apps.dashboard.models.Tag.objects.get_or_create(name='green')[0]
"""


class Connection(models.Model):
     note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note2note')
     source = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='source')
     comment = models.CharField(max_length=200)


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

class NoteTag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
