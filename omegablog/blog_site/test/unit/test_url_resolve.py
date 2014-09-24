from django.core.urlresolvers import resolve, Resolver404
from django.test.testcases import TestCase


class UrlResolve(TestCase):
    def test_url_is_empty___view_is_home(self):
        match = resolve("/")

        self.assertEqual("blog.views.home", match.view_name)

    def test_url_is_blog_entry_with_no_number___404_is_raised(self):
        self.assertRaises(Resolver404, resolve, "/blog_entry")

    def test_url_is_blog_entry_with_non_number_arg___404_is_raised(self):
        self.assertRaises(Resolver404, resolve, "/blog_entry/foo")

    def test_url_is_blog_entry_with_number_arg___view_is_view_entry(self):
        match = resolve("/blog_entry/1")

        self.assertEqual("blog.views.view_entry", match.view_name)

    def test_url_is_blog_entry_with_number_arg___arg_is_correct_number(self):
        match = resolve("/blog_entry/1")

        self.assertEqual('1', match.args[0])

    def test_url_is_create_blog_entry___view_is_modify_entry(self):
        match = resolve("/create_blog_entry")

        self.assertEqual("blog.views.modify_entry", match.view_name)

    def test_url_is_modify_entry_with_no_number___404_is_raised(self):
        self.assertRaises(Resolver404, resolve, "/modify_blog_entry")

    def test_url_is_modify_entry_with_non_number_arg___404_is_raised(self):
        self.assertRaises(Resolver404, resolve, "/modify_blog_entry/foo")

    def test_url_is_modify_entry_with_number_arg___view_is_modify_entry(self):
        match = resolve("/modify_blog_entry/1")

        self.assertEqual("blog.views.modify_entry", match.view_name)

    def test_url_is_modify_entry_with_number_arg___arg_is_correct_number(self):
        match = resolve("/modify_blog_entry/1")

        self.assertEqual('1', match.args[0])

    def test_url_is_delete_entry_with_no_number___404_is_raised(self):
        self.assertRaises(Resolver404, resolve, "/delete_blog_entry")

    def test_url_is_delete_entry_with_non_number_arg___404_is_raised(self):
        self.assertRaises(Resolver404, resolve, "/delete_blog_entry/foo")

    def test_url_is_delete_entry_with_number_arg___view_is_modify_entry(self):
        match = resolve("/delete_blog_entry/1")

        self.assertEqual("blog.views.delete_entry", match.view_name)

    def test_url_is_delete_entry_with_number_arg___arg_is_correct_number(self):
        match = resolve("/delete_blog_entry/1")

        self.assertEqual('1', match.args[0])

    def test_url_is_browse___view_is_browse_entries(self):
        match = resolve("/browse")

        self.assertEqual("blog.views.browse_entries", match.view_name)
