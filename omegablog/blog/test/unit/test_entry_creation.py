from datetime import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import utc
from mock import patch, Mock
from blog.models import Entry


class EntryCreation(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user("user", password="password")
        super(EntryCreation, self).setUp()

    @patch("blog.models.now", Mock(return_value=datetime(2014, 1, 1, tzinfo=utc)))
    def test_entry_is_created___creation_time_is_updated_to_current_time(self):
        Entry(
            title="Title",
            content="Entry Content",
            owner=self.owner,
        ).save()

        entry = Entry.objects.get(title="Title")

        self.assertEqual(datetime(2014, 1, 1, tzinfo=utc), entry.creation_time)

    @patch("blog.models.now", Mock(return_value=datetime(2014, 1, 1, tzinfo=utc)))
    def test_entry_is_created___last_edited_time_is_updated_to_current_time(self):
        Entry(
            title="Title",
            content="Entry Content",
            owner=self.owner,
        ).save()

        entry = Entry.objects.get(title="Title")

        self.assertEqual(datetime(2014, 1, 1, tzinfo=utc), entry.last_edit_time)

    @patch("blog.models.now")
    def test_entry_is_updated___created_time_is_unchanged(self, mock_now):
        def now_time():
            for date in (datetime(2013, 1, 1, tzinfo=utc), datetime(2014, 1, 1, tzinfo=utc)):
                yield date
        mock_now.side_effect = now_time()

        entry = Entry(
            title="Title",
            content="Entry Content",
            owner=self.owner,
        )

        entry.save()
        entry.title = "new title"
        entry.save()

        entry = Entry.objects.get(title="new title")

        self.assertEqual(datetime(2013, 1, 1, tzinfo=utc), entry.creation_time)

    @patch("blog.models.now")
    def test_entry_is_updated___last_edit_time_is_updated(self, mock_now):
        def now_time():
            for date in (datetime(2013, 1, 1, tzinfo=utc), datetime(2014, 1, 1, tzinfo=utc)):
                yield date
        mock_now.side_effect = now_time()

        entry = Entry(
            title="Title",
            content="Entry Content",
            owner=self.owner,
        )

        entry.save()
        entry.title = "new title"
        entry.save()

        entry = Entry.objects.get(title="new title")

        self.assertEqual(datetime(2014, 1, 1, tzinfo=utc), entry.last_edit_time)


