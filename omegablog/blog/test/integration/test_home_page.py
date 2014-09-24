from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from blog.models import Entry
from test_utils.test_case import ServerTestCase
from test_utils.webdriver import wait_for_element, logout


class HomePage(ServerTestCase):
    def setUp(self):
        logout(self.driver, self.live_server_url)
        self.owner = get_user_model().objects.create_user("user", password="password")
        super(HomePage, self).setUp()

    def test_no_blog_entries_present___no_entries_page_is_shown(self):
        self.driver.get(self.live_server_url)

        self.assertIsNotNone(wait_for_element(self.driver, By.ID, "no-blog-entries-title"))

    def test_single_blog_entry_present___entry_is_the_entry(self):
        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        self.driver.get(self.live_server_url)

        self.assertEqual("Test Title", wait_for_element(self.driver, By.ID, "title").text)

    def test_multiple_blog_entry_present___the_latest_created_is_the_entry(self):
        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        Entry(
            title="Second Test Title",
            content="Second Test Content",
            owner=self.owner,
        ).save()

        self.driver.get(self.live_server_url)

        self.assertEqual("Second Test Title", wait_for_element(self.driver, By.ID, "title").text)

    def test_multiple_blog_entry_present_with_earliest_updated___the_latest_updated_is_the_entry(self):
        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        Entry(
            title="Second Test Title",
            content="Second Test Content",
            owner=self.owner,
        ).save()

        entry = Entry.objects.get(title="Test Title")
        entry.title = "Modified Test Title"
        entry.save()

        self.driver.get(self.live_server_url)

        self.assertEqual("Modified Test Title", wait_for_element(self.driver, By.ID, "title").text)

    def test_multiple_blog_entry_present_with_earliest_updated_and_another_created_after___the_latest_created_is_the_entry(self):
        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        Entry(
            title="Second Test Title",
            content="Second Test Content",
            owner=self.owner,
        ).save()

        entry = Entry.objects.get(title="Test Title")
        entry.title = "Modified Test Title"
        entry.save()

        Entry(
            title="Third Test Title",
            content="Third Test Content",
            owner=self.owner,
        ).save()

        self.driver.get(self.live_server_url)

        self.assertEqual("Third Test Title", wait_for_element(self.driver, By.ID, "title").text)
