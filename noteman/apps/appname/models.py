from django.db import models


class Note(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    cr_time = models.DateTimeField()
    type_id = models.IntegerField()
    description = models.CharField(max_length=200)


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
