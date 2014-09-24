from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By

from test_utils.test_case import ServerTestCase
from test_utils.webdriver import login_as, logout, wait_for_element


class BasePage(ServerTestCase):
    def setUp(self):
        logout(self.driver, self.live_server_url)
        super(BasePage, self).setUp()

    def test_click_home_button___navigate_to_home(self):
        self.driver.get(self.live_server_url + "/browse")

        wait_for_element(self.driver, By.ID, "home-link").click()

        self.assertEqual(self.live_server_url + "/", self.driver.current_url)

    def test_click_create_button_while_not_logged_in___navigate_to_login_screen(self):
        self.driver.get(self.live_server_url)

        wait_for_element(self.driver, By.ID, "create-entry-link").click()

        self.assertEqual(self.live_server_url + "/accounts/login/?next=/create_blog_entry", self.driver.current_url)

    def test_click_create_button_while_logged_in___navigate_to_create_screen(self):
        get_user_model().objects.create_user("user", password="password")
        login_as(self.driver, self.live_server_url, "user", "password")
        self.driver.get(self.live_server_url)

        wait_for_element(self.driver, By.ID, "create-entry-link").click()

        self.assertEqual(self.live_server_url + "/create_blog_entry", self.driver.current_url)

    def test_click_browse_button___navigate_to_browse_page(self):
        self.driver.get(self.live_server_url)

        wait_for_element(self.driver, By.ID, "browse-link").click()

        self.assertEqual(self.live_server_url + "/browse", self.driver.current_url)