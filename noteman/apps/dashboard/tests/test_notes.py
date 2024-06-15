from django.test import TestCase

from apps.dashboard.models import Note


class NoteTestCase(TestCase):
    def setUp(self):
        self.base_id = 0
        self.single_note = Note.objects.create(
            name=f'test{self.base_id}',
            type=1,
        )
        self.multiple_notes = [
            Note.objects.create(
                name=f'test{i}',
                type=1,
            )
            for i in range(self.base_id + 1, self.base_id + 1 + 5)
        ]

    def test_single_note(self):
        self.assertTrue(Note.objects.filter(name=self.single_note.name).exists())

    def test_multiple_notes(self):
        self.assertEqual(len(self.multiple_notes), self.base_id + 5 - self.base_id)
        for note in self.multiple_notes:
            self.assertTrue(Note.objects.filter(name=note.name).exists())
