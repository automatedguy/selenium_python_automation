# coding=utf-8
from selenium.webdriver.support.wait import WebDriverWait
from constants import *
from locators import *
from base.setup import logger


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, element, locator, description, obj):
        driver = element.driver
        logger.info(WAITING_FOR_MSG + "[" + description + "] " + obj)
        WebDriverWait(driver, 100).until(lambda driver: driver.find_element_by_xpath(locator))
        return self.driver.find_element_by_xpath(locator)


# Checkout class and sections


class Checkout(BasePage):
    """Checkout Page class"""

    def __init__(self, driver):
        super(Checkout, self).__init__(driver)
        self.driver = driver

    def populate_checkout_info(self):
        """ This method will deal with the initial load """
        PassengerSection(self.driver).populate_passengers()


class PassengerSection(Checkout):
    """"Passenger Section"""

    def __init__(self, driver):
        super(PassengerSection, self).__init__(driver)
        self.driver = driver

    def populate_passengers(self):
        logger.info('Filling Passengers Info.')
        logger.info(FILLING + PassengerSectionLct.NAME_INPUT_DESC)
        self.driver.find_element(*PassengerSectionLct.NAME_INPUT).send_keys('Whatever')


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
        logger.info(CLICKING + LoginModalLct.CLOSE_BUTTON_DESC)
        self.driver.find_element(*LoginModalLct.CLOSE_BUTTON).click()
