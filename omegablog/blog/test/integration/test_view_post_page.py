from time import sleep
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from omegablog.blog.models import Entry
from omegablog.test_utils.test_case import ServerTestCase
from omegablog.test_utils.webdriver import wait_for_element, logout, login_as, wait_for_no_element, wait_for_alert


class ViewPostPage(ServerTestCase):
    def _wait_for_delete(self, pk):
        try:
            count = 0
            while count < 5:
                sleep(1)
                Entry.objects.get(id=pk)
                count += 1
            return False
        except Entry.DoesNotExist:
            return True

    def setUp(self):
        logout(self.driver, self.live_server_url)
        self.owner = get_user_model().objects.create_user("user", password="password")
        self.nonowner = get_user_model().objects.create_user("nonowner", password="password")
        super(ViewPostPage, self).setUp()

    def test_navigate_to_existing_item___correct_title_is_present(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        title_text = wait_for_element(self.driver, By.ID, "title").text
        self.assertEqual("Test Post Title", title_text)

    def test_navigate_to_existing_item___correct_content_is_present(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        content_text = wait_for_element(self.driver, By.ID, "content").text
        self.assertEqual("Test Post Content", content_text)

    def test_navigate_to_existing_item_as_owner___edit_button_is_present(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "user", "password")

        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        self.assertIsNotNone(wait_for_element(self.driver, By.ID, "edit-button"))

    def test_navigate_to_existing_item_as_non_owner___edit_button_is_not_present(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "nonowner", "password")

        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        self.assertTrue(wait_for_no_element(self.driver, By.ID, "edit-button"))

    def test_navigate_to_existing_item_not_logged_in___edit_button_is_not_present(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        self.assertTrue(wait_for_no_element(self.driver, By.ID, "edit-button"))

    def test_click_edit_button___taken_to_edit_page(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        wait_for_element(self.driver, By.ID, "edit-button").click()

        self.assertEqual(self.live_server_url + "/modify_blog_entry/" + str(pk), self.driver.current_url)

    def test_navigate_to_existing_item_as_owner___delete_button_is_present(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "user", "password")

        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        self.assertIsNotNone(wait_for_element(self.driver, By.ID, "delete-button"))

    def test_navigate_to_existing_item_as_non_owner___delete_button_is_not_present(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "nonowner", "password")

        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        self.assertTrue(wait_for_no_element(self.driver, By.ID, "delete-button"))

    def test_navigate_to_existing_item_not_logged_in___delete_button_is_not_present(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        self.assertTrue(wait_for_no_element(self.driver, By.ID, "delete-button"))

    def test_click_delete_button_and_cancel___entry_is_not_deleted(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        wait_for_element(self.driver, By.ID, "delete-button").click()
        wait_for_alert(self.driver).dismiss()

        self.assertIsNotNone(Entry.objects.get(id=pk))

    def test_click_delete_button_and_cancel___page_is_not_changed(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        wait_for_element(self.driver, By.ID, "delete-button").click()
        wait_for_alert(self.driver).dismiss()

        self.assertEqual(self.live_server_url + "/blog_entry/" + str(pk), self.driver.current_url)

    def test_click_delete_button_and_accept___entry_has_been_deleted(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        wait_for_element(self.driver, By.ID, "delete-button").click()
        wait_for_alert(self.driver).accept()

        self.assertTrue(self._wait_for_delete(pk))

    def test_click_delete_button_and_accept___redirected_home(self):
        Entry(
            title="Test Post Title",
            content="Test Post Content",
            owner=self.owner,
        ).save()

        pk = Entry.objects.first().id

        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url + "/blog_entry/" + str(pk))
        wait_for_element(self.driver, By.ID, "delete-button").click()
        wait_for_alert(self.driver).accept()
        self._wait_for_delete(pk)

        self.assertEqual(self.live_server_url + "/", self.driver.current_url)

