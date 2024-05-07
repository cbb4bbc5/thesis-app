import django.utils

from django.db import models
from django.db.models.functions import Now


class Note(models.Model):
    # TODO: note name probably should be unique since it is supposed to be file path in the end
    name = models.CharField(max_length=200)
    # db_default or default
    # https://stackoverflow.com/questions/77665050/what-does-the-new-field-db-default-of-django-5-imply-should-we-use-it-by-def
    cr_time = models.DateTimeField(default=django.utils.timezone.now)
    # TODO: use choices for type_id, like here
    # https://stackoverflow.com/questions/48040008/django-restrict-data-that-can-be-given-to-model-field
    type = models.IntegerField()
    description = models.TextField(blank=True)

"""Example code (copy for tests)
import apps.dashboard.models

n1 = apps.dashboard.models.Note.objects.get_or_create(name='First note', type=1, description='this is a first note')[0]
n2 = apps.dashboard.models.Note.objects.get_or_create(name='Second note', type=1, description='this is a second note')[0]
n3 = apps.dashboard.models.Note.objects.get_or_create(name='Third note', type=1, description='this is a third note')[0]

t1 = apps.dashboard.models.Tag.objects.get_or_create(name='red')[0]
t2 = apps.dashboard.models.Tag.objects.get_or_create(name='blue')[0]
t3 = apps.dashboard.models.Tag.objects.get_or_create(name='green')[0]
but better to create it from the dashboard
"""


class Connection(models.Model):
     note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note')
     source = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='source')
     comment = models.TextField(blank=True)

     class Meta:
         # https://stackoverflow.com/questions/63649333/how-to-add-constraint-for-2-fields-not-having-the-same-value
         # TODO: also take into account avoiding cycles but probably not as a constraint? I need to think this through
         constraints = [
             models.CheckConstraint(
                 check=~models.Q(note=models.F('source')),
                 name='not_equal'
             ),
             models.UniqueConstraint(
                 fields=['note', 'source'], name='unique_sources'
             )
         ]


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_tag_name'
            )
        ]


class NoteTag(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            # https://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
            # good replacement for composite primary key in django
            models.UniqueConstraint(
                fields=['note', 'tag'], name='unique_tags'
            ),
        ]
