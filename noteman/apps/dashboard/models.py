from datetime import datetime as dt

from django.db import models
from django.db.models.functions import Now


class Note(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    # db_default or default
    # https://stackoverflow.com/questions/77665050/what-does-the-new-field-db-default-of-django-5-imply-should-we-use-it-by-def
    cr_time = models.DateTimeField(db_default=Now())
    # TODO: use choices for type_id, like here
    # https://stackoverflow.com/questions/48040008/django-restrict-data-that-can-be-given-to-model-field
    type_id = models.IntegerField()
    description = models.CharField(max_length=200)

    @classmethod
    def gen_id(cls) -> str:
        return 'D' + str(dt.now().replace(microsecond=0)).replace(' ', 'H')


class Source(models.Model):
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    # because 255 is the max path length most fs can handle
    source_URL = models.CharField(max_length=255)


class TagName(models.Model):
    tag_name = models.CharField(max_length=50)
    # might be changed later


class Tag(models.Model):
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(TagName, on_delete=models.CASCADE)


class NoteType(models.Model):
    type_name = models.CharField(max_length=50)
    # definitely shorter than 50 but I will change that later


class EditHistory(models.Model):
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
