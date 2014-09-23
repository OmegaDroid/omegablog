from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponseForbidden
from django.test import TestCase
from omegablog.blog.models import Entry
from omegablog.blog.views import delete_entry


class ViewDeleteEntry(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user("user", password="password")
        self.nonowner = get_user_model().objects.create_user("nonowner", password="password")
        super(ViewDeleteEntry, self).setUp()

    def test_user_in_request_is_not_owner___403_is_returned(self):
        request = HttpRequest()
        request.user = self.nonowner

        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        self.assertIsInstance(delete_entry(request, pk), HttpResponseForbidden)