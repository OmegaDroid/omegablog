from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


DEFAULT_TIMEOUT = 5


def wait_for_element(driver, by, value, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, value)))


def wait_for_all_elements(driver, by, value, timeout=DEFAULT_TIMEOUT):
    WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, value)))
    return driver.find_elements(by, value)


def wait_for_no_element(driver, by, value, timeout=DEFAULT_TIMEOUT):
    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, value)))
        return False
    except TimeoutException:
        return True


def wait_for_alert(driver, timeout=DEFAULT_TIMEOUT):
    WebDriverWait(driver, timeout).until(ec.alert_is_present())
    return driver.switch_to.alert


def logout(driver, server_address):
    driver.get(server_address)
    try:
        wait_for_element(driver, By.ID, "logout-link", timeout=0).click()
    except TimeoutException:
        pass


def login_as(driver, server_address, username, password):
    logout(driver, server_address)
    wait_for_element(driver, By.ID, "login-link").click()
    wait_for_element(driver, By.NAME, "username").send_keys(username)
    wait_for_element(driver, By.NAME, "password").send_keys(password)
    wait_for_element(driver, By.NAME, "submit").click()
