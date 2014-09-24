from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from blog.models import Entry
from blog_utils.queries import first_or_none


class QueriesFirstOrNone(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user("user", password="password")

    def test_no_objects_created___result_is_none(self):
        self.assertIsNone(first_or_none(Entry.objects.all()))

    def test_no_single_object_created___result_is_object(self):
        Entry(
            title="First Title",
            content="First Content",
            owner=self.owner,
        ).save()

        self.assertEqual(Entry.objects.get(title="First Title"), first_or_none(Entry.objects.all()))

    def test_two_objects_created___result_is_first_created_object(self):
        Entry(
            title="First Title",
            content="First Content",
            owner=self.owner,
        ).save()

        Entry(
            title="Second Title",
            content="Second Content",
            owner=self.owner,
        ).save()

        self.assertEqual(Entry.objects.get(title="First Title"), first_or_none(Entry.objects.all()))

    def test_two_objects_created_accessed_in_reverse_order___result_is_second_created_object(self):
        Entry(
            title="First Title",
            content="First Content",
            owner=self.owner,
        ).save()

        Entry(
            title="Second Title",
            content="Second Content",
            owner=self.owner,
        ).save()

        self.assertEqual(Entry.objects.get(title="Second Title"), first_or_none(Entry.objects.all().order_by("-id")))
