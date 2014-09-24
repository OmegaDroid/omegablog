from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


DEFAULT_TIMEOUT = 5  # The default timeout for all webdriver actions is 5 seconds


def wait_for_element(driver, by, value, timeout=DEFAULT_TIMEOUT):
    """
    Waits for an element to be present on the page and returns it. If the element is not fount a TimeoutException is
    raised.

    :param driver: The selenium web driver object.
    :param by: The property to search for (see selenium.webdriver.common.by.By)
    :param value: The value to search for
    :param timeout: The time to wait to find the object
    :return: The found element
    """
    return WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, value)))


def wait_for_all_elements(driver, by, value, timeout=DEFAULT_TIMEOUT):
    """
    Waits for an element to be present on the page and returns all that match the criteria. If no element is not fount a
    TimeoutException is raised.

    :param driver: The selenium web driver object.
    :param by: The property to search for (see selenium.webdriver.common.by.By)
    :param value: The value to search for
    :param timeout: The time to wait to find the object
    :return: The found elements
    """
    WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, value)))
    return driver.find_elements(by, value)


def wait_for_no_element(driver, by, value, timeout=DEFAULT_TIMEOUT):
    """
    Waits for an element to not be seen on the page. This waits for the timeout time to give time for elements to
    appear.

    :param driver: The selenium web driver object.
    :param by: The property to search for (see selenium.webdriver.common.by.By)
    :param value: The value to search for
    :param timeout: The time to wait to find the object
    :return: True of the element was not found, False otherwise
    """
    try:
        WebDriverWait(driver, timeout).until(ec.presence_of_element_located((by, value)))
        return False
    except TimeoutException:
        return True


def wait_for_alert(driver, timeout=DEFAULT_TIMEOUT):
    """
    Waits wor an alert to be present on the screen, if no alert is present within the timeout a TimeoutException is
    raised

    :param driver: The selenium web driver object.
    :param timeout: The time to wait to find the object
    :return: The alert object
    """
    WebDriverWait(driver, timeout).until(ec.alert_is_present())
    return driver.switch_to.alert


def logout(driver, server_address):
    """
    Logs out of the site through the web interface. If no logout link is found no action is taken

    :param driver: The selenium web driver object.
    :param server_address: The address of the server
    """
    driver.get(server_address)
    try:
        wait_for_element(driver, By.ID, "logout-link", timeout=0).click()
    except TimeoutException:
        pass


def login_as(driver, server_address, username, password):
    """
    Logs into the site through the web interface. If the user is currently logged in they are first logged out.

    :param driver: The selenium web driver object.
    :param server_address: The address of the server
    :param username: The user to login as
    :param password: The password for the user
    """
    logout(driver, server_address)
    wait_for_element(driver, By.ID, "login-link").click()
    wait_for_element(driver, By.NAME, "username").send_keys(username)
    wait_for_element(driver, By.NAME, "password").send_keys(password)
    wait_for_element(driver, By.NAME, "submit").click()
