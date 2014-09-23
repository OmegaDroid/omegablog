from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from omegablog.blog.models import Entry
from omegablog.test_utils.test_case import ServerTestCase
from omegablog.test_utils.webdriver import logout, wait_for_element, login_as


class CreateEntryPage(ServerTestCase):
    def setUp(self):
        logout(self.driver, self.live_server_url)
        get_user_model().objects.create_user("user", password="password")
        super(CreateEntryPage, self).setUp()

    def test_not_logged_in_click_create_entry___taken_to_login_page(self):
        wait_for_element(self.driver, By.ID, "create-entry-link").click()

        self.assertEqual(self.live_server_url + "/accounts/login/?next=/create_blog_entry", self.driver.current_url)

    def test_logged_in_click_create_entry___taken_to_create_entry_form(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()

        self.assertEqual(self.live_server_url + "/create_blog_entry", self.driver.current_url)

    def test_navigate_to_create_entry_form___title_field_is_present(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()

        self.assertIsNotNone(wait_for_element(self.driver, By.NAME, "title"))

    def test_navigate_to_create_entry_form___content_field_is_present(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()

        self.assertIsNotNone(wait_for_element(self.driver, By.NAME, "content"))

    def test_submit_create_form_with_no_title___field_is_in_error(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()
        wait_for_element(self.driver, By.NAME, "content").send_keys("some content")
        wait_for_element(self.driver, By.NAME, "submit").click()

        form_group = wait_for_element(self.driver, By.XPATH, ".//*[@name='title']/..")
        self.assertIn("has-error", form_group.get_attribute("class"))

    def test_submit_create_form_with_no_title___content_is_unchanged(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()
        wait_for_element(self.driver, By.NAME, "content").send_keys("some content")
        wait_for_element(self.driver, By.NAME, "submit").click()

        self.assertEqual("some content", wait_for_element(self.driver, By.NAME, "content").text)

    def test_submit_create_form_with_no_content___field_is_in_error(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()
        wait_for_element(self.driver, By.NAME, "title").send_keys("some title")
        wait_for_element(self.driver, By.NAME, "submit").click()

        form_group = wait_for_element(self.driver, By.XPATH, ".//*[@name='content']/..")
        self.assertIn("has-error", form_group.get_attribute("class"))

    def test_submit_create_form_with_no_content___title_is_unchanged(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()
        wait_for_element(self.driver, By.NAME, "title").send_keys("some title")
        wait_for_element(self.driver, By.NAME, "submit").click()

        self.assertEqual("some title", wait_for_element(self.driver, By.NAME, "title").get_attribute("value"))

    def test_submit_valid_form___new_model_object_is_created(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()
        wait_for_element(self.driver, By.NAME, "title").send_keys("some title")
        wait_for_element(self.driver, By.NAME, "content").send_keys("some content")
        wait_for_element(self.driver, By.NAME, "submit").click()

        self.assertIsNotNone(Entry.objects.get(title="some title", content="some content"))

    def test_submit_valid_form___redirected_to_the_blog_entry(self):
        login_as(self.driver, self.live_server_url, "user", "password")

        wait_for_element(self.driver, By.ID, "create-entry-link").click()
        wait_for_element(self.driver, By.NAME, "title").send_keys("some title")
        wait_for_element(self.driver, By.NAME, "content").send_keys("some content")
        wait_for_element(self.driver, By.NAME, "submit").click()

        pk = Entry.objects.get(title="some title", content="some content").pk
        self.assertEqual(self.live_server_url + "/blog_entry/" + str(pk), self.driver.current_url)
