from django.http import HttpRequest, Http404
from django.test import TestCase
from omegablog.blog.views import view_entry


class ViewEntry(TestCase):
    def test_primary_key_is_not_in_database___404_error_is_raised(self):
        request = HttpRequest()

        self.assertRaises(Http404, view_entry, request, 123)
