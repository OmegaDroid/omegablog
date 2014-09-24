from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.timezone import utc
from mock import patch, Mock
from selenium.webdriver.common.by import By
from blog.models import Entry
from test_utils.test_case import ServerTestCase
from test_utils.webdriver import logout, wait_for_no_element, wait_for_all_elements, wait_for_element


class BrowsePage(ServerTestCase):
    def setUp(self):
        logout(self.driver, self.live_server_url)
        self.owner = get_user_model().objects.create_user("user", password="password")
        super(BrowsePage, self).setUp()

    def test_no_blog_entries_created___no_blog_entries_are_present(self):
        self.driver.get(self.live_server_url + "/browse")

        self.assertTrue(wait_for_no_element(self.driver, By.CLASS_NAME, "blog-listing-entry"))

    def test_single_blog_entry_created___that_entry_is_the_only_listed_entry(self):
        Entry(
            title="First Test Entry",
            content="First Test Content",
            owner=self.owner,
        ).save()

        self.driver.get(self.live_server_url + "/browse")

        entries = wait_for_all_elements(self.driver, By.CLASS_NAME, "blog-listing-entry")
        num_entries = len(entries)
        title = entries[0].find_element(By.CLASS_NAME, "title").text

        self.assertEqual(1, num_entries)
        self.assertEqual("First Test Entry", title)

    def test_click_entry_title___that_entry_loaded(self):
        Entry(
            title="First Test Entry",
            content="First Test Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.get(title="First Test Entry").id

        self.driver.get(self.live_server_url + "/browse")
        wait_for_element(self.driver, By.CSS_SELECTOR, ".blog-listing-entry .title").click()

        self.assertEqual(self.live_server_url + "/blog_entry/" + str(pk), self.driver.current_url)

    @patch("blog.models.now", Mock(return_value=datetime(2014, 1, 2, 21, 12, tzinfo=utc)))
    def test_single_blog_entry_created___published_time_is_present_in_listing_entry(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        self.driver.get(self.live_server_url + "/browse")
        publish_time = wait_for_element(self.driver, By.CSS_SELECTOR, ".blog-listing-entry .publish-time").text

        self.assertEqual("Published: 02 Jan 2014 21:12:00", publish_time)

    @patch("blog.models.now")
    def test_single_blog_entry_created_and_modified___published_time_is_present_in_listing_entry(self, mock_now):
        def now_time():
            for date in (datetime(2013, 2, 3, 4, 5, 6, tzinfo=utc), datetime(2014, 7, 8, 9, 10, 11, tzinfo=utc)):
                yield date
        mock_now.side_effect = now_time()

        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        entry = Entry.objects.all()[0]
        pk = entry.id
        entry.title = "Modified Title"
        entry.save()

        self.driver.get(self.live_server_url + "/browse")
        publish_time = wait_for_element(self.driver, By.CSS_SELECTOR, ".blog-listing-entry .publish-time").text

        self.assertEqual("Published: 03 Feb 2013 04:05:06 (Edit: 08 Jul 2014 09:10:11)", publish_time)

    def test_two_blog_entries_created___both_entries_are_listed_in_the_correct_order(self):
        Entry(
            title="First Test Entry",
            content="First Test Content",
            owner=self.owner,
        ).save()

        Entry(
            title="Second Test Entry",
            content="Second Test Content",
            owner=self.owner,
        ).save()

        self.driver.get(self.live_server_url + "/browse")

        entries = wait_for_all_elements(self.driver, By.CLASS_NAME, "blog-listing-entry")
        num_entries = len(entries)
        titles = [entry.find_element(By.CLASS_NAME, "title").text for entry in entries]

        self.assertEqual(2, num_entries)
        self.assertEqual("Second Test Entry", titles[0])
        self.assertEqual("First Test Entry", titles[1])

    def test_two_blog_entries_created_one_is_modified___both_entries_are_listed_in_the_correct_order_with_modified_first(self):
        Entry(
            title="First Test Entry",
            content="First Test Content",
            owner=self.owner,
        ).save()

        Entry(
            title="Second Test Entry",
            content="Second Test Content",
            owner=self.owner,
        ).save()

        entry = Entry.objects.get(title="First Test Entry")
        entry.title = "Modified Test Entry"
        entry.save()

        self.driver.get(self.live_server_url + "/browse")

        entries = wait_for_all_elements(self.driver, By.CLASS_NAME, "blog-listing-entry")
        num_entries = len(entries)
        titles = [entry.find_element(By.CLASS_NAME, "title").text for entry in entries]

        self.assertEqual(2, num_entries)
        self.assertEqual("Modified Test Entry", titles[0])
        self.assertEqual("Second Test Entry", titles[1])

