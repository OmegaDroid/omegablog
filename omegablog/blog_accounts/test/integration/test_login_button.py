from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By

from test_utils.test_case import ServerTestCase
from test_utils.webdriver import logout, wait_for_element, login_as


class LoginButton(ServerTestCase):
    def setUp(self):
        logout(self.driver, self.live_server_url)
        self.driver.get(self.live_server_url)

    def test_user_not_logged_in___login_button_is_present(self):
        self.assertIsNotNone(wait_for_element(self.driver, By.ID, "login-link"))

    def test_user_clicks_login___taken_to_login_screen(self):
        wait_for_element(self.driver, By.ID, "login-link").click()

        self.assertEqual(self.live_server_url + "/accounts/login/?next=/", self.driver.current_url)

    def test_logs_in_as_user___taken_back_to_home_screen(self):
        get_user_model().objects.create_user("user", password="password")

        login_as(self.driver, self.live_server_url, "user", "password")

        self.assertEqual(self.live_server_url + "/", self.driver.current_url)

    def test_logs_in_as_user___login_button_changes_to_logout(self):
        get_user_model().objects.create_user("user", password="password")

        login_as(self.driver, self.live_server_url, "user", "password")

        self.assertIsNotNone(wait_for_element(self.driver, By.ID, "logout-link"))

    def test_click_logout_button___login_button_is_visible(self):
        get_user_model().objects.create_user("user", password="password")

        login_as(self.driver, self.live_server_url, "user", "password")
        wait_for_element(self.driver, By.ID, "logout-link").click()

        self.assertIsNotNone(wait_for_element(self.driver, By.ID, "login-link"))
