# coding=utf-8

import logging
from selenium.webdriver.support.wait import WebDriverWait
from constants import CLICKING, WAITING_FOR_MSG
from locators import LoginModalLocators


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, element, locator, description, obj):
        driver = element.driver
        self.logger.info(WAITING_FOR_MSG + "[" + description + "] " + obj)
        WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath(locator))
        return self.driver.find_element_by_xpath(locator)

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)


# Checkout class and sections


class Checkout(BasePage):
    """Checkout Page class"""

    def __init__(self, driver):
        super(Checkout, self).__init__(driver)
        self.driver = driver


class PassengerSection(Checkout):
    """"Passenger Section"""

    def __init__(self, driver):
        super(PassengerSection, self).__init__(driver)
        self.driver = driver


class PaymentSection(Checkout):
    """Payment Section"""

    def __init__(self, driver):
        super(PaymentSection, self).__init__(driver)
        self.driver = driver


# Home page and sections

class Home(BasePage):
    """Home Page class"""


class LoginModal(BasePage):
    """ Login Modal class"""

    def __init__(self, driver):
        super(LoginModal, self).__init__(driver)
        self.driver = driver

    def click_close_login_modal(self):
        self.logger.info(CLICKING + LoginModalLocators.CLOSE_BUTTON_DESC)
        self.driver.find_element(*LoginModalLocators.CLOSE_BUTTON).click()
