from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ServerTestCase(TestCase, LiveServerTestCase):
    """
    Need to inherit from both TestCase and StaticLiveServerCase
    so that the database is also reset
    """
    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        LiveServerTestCase.setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        LiveServerTestCase.tearDownClass()
