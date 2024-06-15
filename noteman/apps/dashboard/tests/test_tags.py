from django.db import IntegrityError
from django.test import TestCase

from apps.dashboard.models import Tag


class TagTestCase(TestCase):
    def setUp(self):
        self.single_tag = Tag.objects.create(
            name='tag0',
        )

    def test_single_tag(self):
        self.assertTrue(Tag.objects.filter(name=self.single_tag.name).exists())

    def test_readding_tag(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises
        with self.assertRaises(IntegrityError) as cm:
            Tag.objects.create(
                name=self.single_tag.name,
            )
