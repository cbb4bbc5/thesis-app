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
    TEXT = 1
    PDF = 2
    VIDEO = 3
    AUDIO = 4
    URL = 5
    TYPE_CHOICES = {
        TEXT: "Local text file",
        PDF: "Local PDF (or similar) file",
        VIDEO: "Local video file",
        AUDIO: "Local audio file",
        URL: "External link",
    }
    name = models.CharField(max_length=200)
    cr_time = models.DateTimeField(default=django.utils.timezone.now,
                                   verbose_name='creation time')
    type = models.IntegerField(
        choices=TYPE_CHOICES,
        default=TEXT,
    )
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
