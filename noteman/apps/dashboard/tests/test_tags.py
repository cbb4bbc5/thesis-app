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

        # maybe TODO: check the error code as well but this seems to be more trouble
        # that it would be worth
        # the_exception = cm.exception
        # https://www.postgresql.org/docs/current/errcodes-appendix.html
        # print(the_exception.args)
