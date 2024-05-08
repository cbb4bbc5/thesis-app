from django.db import IntegrityError
from django.test import TestCase

from apps.dashboard.models import Note, Tag, NoteTag

class NoteTagTestCase(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            name='note',
            type=1
        )
        self.base_id = 0
        self.range_len = 3
        self.tag = Tag.objects.create(
            name=f'tag{self.base_id}',
        )
        self.notetags = NoteTag.objects.create(
            note=self.note,
            tag=self.tag,
        )
        self.tags = [
            Tag.objects.create(name=f'tag{i}')
            for i in range(self.base_id + 1, self.base_id + 1 + self.range_len)
        ]
        for t in self.tags:
            NoteTag.objects.create(
                note=self.note,
                tag=t,
            )

    def test_add_tag(self):
        self.assertTrue(NoteTag.objects.filter(note=self.note, tag=self.tag).exists())


    def test_add_multiple_tags(self):
        for t in self.tags:
            self.assertTrue(NoteTag.objects.filter(note=self.note, tag=t).exists)


    def test_readd_tag(self):
        with self.assertRaises(IntegrityError) as cm:
            NoteTag.objects.create(
                note=self.note,
                tag=self.tag,
            )
