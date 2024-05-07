from django.test import TestCase

from apps.dashboard.models import Note


# TODO: find better way
# command for running tests docker compose run noteman python manage.py test apps/dashboard/tests
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
                type=1
            )
            for i in range(self.base_id + 1, self.base_id + 1 + 5)
        ]


# https://docs.python.org/3/library/unittest.html#assert-methods
    def test_single_note(self):
        self.assertTrue(Note.objects.filter(name=self.single_note.name).exists())


    def test_multiple_notes(self):
        self.assertEqual(len(self.multiple_notes), self.base_id + 5 - self.base_id)
        for note in self.multiple_notes:
            self.assertTrue(Note.objects.filter(name=note.name).exists())

# from django.test import TestCase

# from apps.dashboard.models import Note, Source


# class NoteTestCase(TestCase):
#     def setUp(self):
#         self.scratch_id = Note.gen_id()
#         Note.objects.create(
#             id=self.scratch_id,
#             type_id=1,
#             description='this is a test note',
#         )


#     def test_note_retrieval(self):
#         "Test retrieving notes by id"
#         # there should only be one note of given id so I used get
#         scratch_note = Note.objects.get(id=self.scratch_id)
#         self.assertEqual(scratch_note.type_id, 1)
#         self.assertEqual(scratch_note.description, 'this is a test note')
        

# class SourceTestCase(TestCase):
#     def setUp(self):
#         for num in range(1, 5):
#             Note.objects.create(
#                 id=num * 'a',
#                 type_id=1,
#                 description=f'a test note number {num}',
#             )

#         Note.objects.create(
#             id='b',
#             type_id=1,
#             description=f'a test note number {num}',
#         )
#         self.long_note_id = 'long_note'
#         self.short_notes = Note.objects.filter(id__startswith='a')
#         self.long_note = Note.objects.create(
#             id=self.long_note_id,
#             type_id=2,
#             description='this is a longer note'
#         )

#         for s in self.short_notes:
#             Source.objects.create(
#                 note_id=self.long_note,
#                 source_URL=s.id,
#             )

#     def test_existing_sources(self):
#         "Tests whether a note has correct sources"
#         self.sources = Source.objects.filter(note_id=self.long_note_id)
#         self.assertEqual(len(self.sources), len(self.short_notes))
#         self.assertEqual(len(self.sources), 4)
