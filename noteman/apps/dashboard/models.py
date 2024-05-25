import django.utils
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_tag_name'
            )
        ]

    def __str__(self):
        return f'{self.name}'


class Note(models.Model):
    # TODO: note name probably should be unique since it is supposed to be file path in the end
    name = models.CharField(max_length=200)
    # db_default or default
    # https://stackoverflow.com/questions/77665050/what-does-the-new-field-db-default-of-django-5-imply-should-we-use-it-by-def
    cr_time = models.DateTimeField(default=django.utils.timezone.now,
                                   verbose_name='creation time')
    # TODO: use choices for type_id, like here
    # https://stackoverflow.com/questions/48040008/django-restrict-data-that-can-be-given-to-model-field
    type = models.IntegerField()
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, through="NoteTag")
    references = models.ManyToManyField(
        "Note", through="Connection", symmetrical=False, related_name="related_to"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'], name='unique_note_name'
            ),
        ]

    def __str__(self):
        return f'{self.name}'


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
