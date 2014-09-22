from selenium.webdriver.common.by import By

from omegablog.test_utils.test_case import ServerTestCase
from omegablog.test_utils.webdriver import logout, wait_for_element


class LoginButton(ServerTestCase):
    def setUp(self):
        logout(self.driver, self.live_server_url)
        self.driver.get(self.live_server_url)

    def test_user_not_logged_in___login_button_is_present(self):
        self.assertIsNotNone(wait_for_element(self.driver, By.ID, "login-button"))

    def test_user_clicks_login___taken_to_login_screen(self):
        wait_for_element(self.driver, By.ID, "login-button").click()

        self.assertEqual(self.live_server_url + "/login", self.driver.current_url)


