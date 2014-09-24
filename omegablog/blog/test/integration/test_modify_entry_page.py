from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.timezone import utc
from mock import patch
from selenium.webdriver.common.by import By
from blog.models import Entry
from test_utils.test_case import ServerTestCase
from test_utils.webdriver import wait_for_element, logout, login_as


class ModifyEntryPage(ServerTestCase):
    def setUp(self):
        logout(self.driver, self.live_server_url)
        self.owner = get_user_model().objects.create_user("user", password="password")
        super(ModifyEntryPage, self).setUp()

    def test_navigate_to_edit_page___title_is_correct(self):
        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.all()[0].id

        login_as(self.driver, self.live_server_url, "user", "password")

        self.driver.get(self.live_server_url + "/modify_blog_entry/" + str(pk))
        title_text = wait_for_element(self.driver, By.NAME, "title").get_attribute("value")
        self.assertEqual("Test Title", title_text)

    def test_navigate_to_edit_page___content_is_correct(self):
        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.all()[0].id

        login_as(self.driver, self.live_server_url, "user", "password")

        self.driver.get(self.live_server_url + "/modify_blog_entry/" + str(pk))
        content_text = wait_for_element(self.driver, By.NAME, "content").text
        self.assertEqual("Test Content", content_text)

    def test_title_is_changed___title_is_updated(self):
        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.all()[0].id

        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url + "/modify_blog_entry/" + str(pk))
        wait_for_element(self.driver, By.NAME, "title").send_keys(" more")
        wait_for_element(self.driver, By.NAME, "submit").click()

        entry = Entry.objects.get(id=pk)
        self.assertEqual("Test Title more", entry.title)

    def test_content_is_changed___content_is_updated(self):
        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.all()[0].id

        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url + "/modify_blog_entry/" + str(pk))
        wait_for_element(self.driver, By.NAME, "content").send_keys(" more")
        wait_for_element(self.driver, By.NAME, "submit").click()

        entry = Entry.objects.get(id=pk)
        self.assertEqual("Test Content more", entry.content)

    @patch("blog.models.now")
    def test_post_is_changed___last_edited_is_updated(self, mock_now):
        def now_time():
            for date in (datetime(2013, 1, 1, tzinfo=utc), datetime(2014, 1, 1, tzinfo=utc)):
                yield date
        mock_now.side_effect = now_time()

        Entry(
            title="Test Title",
            content="Test Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.all()[0].id

        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url + "/modify_blog_entry/" + str(pk))
        wait_for_element(self.driver, By.NAME, "content").send_keys(" more")
        wait_for_element(self.driver, By.NAME, "submit").click()

        entry = Entry.objects.get(id=pk)
        self.assertEqual(datetime(2014, 1, 1, tzinfo=utc), entry.last_edit_time)