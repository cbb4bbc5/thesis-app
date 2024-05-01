from datetime import datetime as dt

from django.db import models
from django.db.models.functions import Now


class Note(models.Model):
    name = models.CharField(max_length=200)
    # db_default or default
    # https://stackoverflow.com/questions/77665050/what-does-the-new-field-db-default-of-django-5-imply-should-we-use-it-by-def
    cr_time = models.DateTimeField(db_default=Now())
    # TODO: use choices for type_id, like here
    # https://stackoverflow.com/questions/48040008/django-restrict-data-that-can-be-given-to-model-field
    type_id = models.IntegerField()
    description = models.CharField(max_length=200)


class Connection(models.Model):
     notes = models.ManyToManyField(Note, related_name='note2notes')
     sources = models.ManyToManyField(Note, related_name='sources')
     comment = models.CharField(max_length=200)
