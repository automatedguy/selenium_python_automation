# coding=utf-8
import logging
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from constants import *
from locators import *

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


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
    # Locators
    name_lct = PassengerSectionLct.NAME
    name_desc = PassengerSectionLct.NAME_DESC

    last_name_lct = PassengerSectionLct.LAST_NAME
    last_name_desc = PassengerSectionLct.LAST_NAME_DESC

    document_type_lct = PassengerSectionLct.DOCUMENT_TYPE
    document_type_desc = PassengerSectionLct.DOCUMENT_TYPE_DESC

    document_number_lct = PassengerSectionLct.DOCUMENT_NUMBER
    document_number_desc = PassengerSectionLct.DOCUMENT_NUMBER_DESC

    birthday_lct = PassengerSectionLct.BIRTHDAY
    birthday_desc = PassengerSectionLct.BIRTHDAY_DESC

    birthmonth_lct = PassengerSectionLct.BIRTHMONTH
    birthmonth_desc = PassengerSectionLct.BIRTHMONTH_DESC

    birthyear_lct = PassengerSectionLct.BIRTHYEAR
    birthyear_desc = PassengerSectionLct.BIRTHYEAR_DESC

    gender_lct = PassengerSectionLct.GENDER
    gender_desc = PassengerSectionLct.GENDER_DESC

    nationality_lct = PassengerSectionLct.NATIONALITY
    nationality_desc = PassengerSectionLct.NATIONALITY_DESC

    def __init__(self, driver):
        super(PassengerSection, self).__init__(driver)
        self.driver = driver

    def set_name(self, passenger_index, passenger_name):
        logger.info(FILLING + self.name_desc + passenger_name)
        self.driver.find_elements(*self.name_lct)[passenger_index].send_keys(passenger_name)

    def set_last_name(self, passenger_index, passenger_last_name):
        logger.info(FILLING + self.last_name_desc + passenger_last_name)
        self.driver.find_elements(*self.last_name_lct)[passenger_index].send_keys(passenger_last_name)

    def set_document_type(self, passenger_index, passenger_document_type):
        logger.info(SELECTING + self.document_type_desc + passenger_document_type)
        Select(self.driver.find_elements(*self.document_type_lct)[passenger_index])\
            .select_by_visible_text(passenger_document_type)

    def set_document_number(self, passenger_index, passenger_document_number):
        logger.info(FILLING + self.document_number_desc + passenger_document_number)
        self.driver.find_elements(*self.document_number_lct)[passenger_index].send_keys(passenger_document_number)

    def select_birthday(self, passenger_index, passenger_birthday):
        logger.info(SELECTING + self.birthday_desc + passenger_birthday)
        Select(self.driver.find_elements(*self.birthday_lct)[passenger_index])\
            .select_by_visible_text(passenger_birthday)

    def select_birthmonth(self, passenger_index, passenger_birthmonth):
        logger.info(SELECTING + self.birthmonth_desc + passenger_birthmonth)
        Select(self.driver.find_elements(*self.birthmonth_lct)[passenger_index])\
            .select_by_visible_text(passenger_birthmonth)

    def select_birthyear(self, passenger_index, passenger_birthyear):
        logger.info(SELECTING + self.birthyear_desc + passenger_birthyear)
        Select(self.driver.find_elements(*self.birthyear_lct)[passenger_index])\
            .select_by_visible_text(passenger_birthyear)

    def select_gender(self, passenger_index, passenger_gender):
        logger.info(SELECTING + self.gender_desc + passenger_gender)
        Select(self.driver.find_elements(*self.gender_lct)[passenger_index])\
            .select_by_visible_text(passenger_gender)

    def select_nationality(self, passenger_index, passenger_nationality):
        logger.info(SELECTING + self.nationality_desc + passenger_nationality)
        Select(self.driver.find_elements(*self.nationality_lct)[passenger_index])\
            .select_by_visible_text(passenger_nationality)

    def populate_passengers(self):

        total_passengers = len(self.driver.find_elements(*PassengerSectionLct.NAME))

        Utils().print_separator()
        logger.info("Filling Passengers info - Total Passengers: " + str(total_passengers))
        Utils().print_separator()

        for passenger in range(0, total_passengers):
            logger.info('Filling Passenger N°: ' + str(passenger + 1))

            self.set_name(passenger, 'Whatever')
            self.set_last_name(passenger, 'Nevermind')
            self.set_document_type(passenger, 'Pasaporte')
            self.set_document_number(passenger, '23456543N')
            self.select_birthday(passenger, '1')
            self.select_birthmonth(passenger, 'Enero')
            self.select_birthyear(passenger, '1990')
            self.select_gender(passenger, 'Masculino')
            self.select_nationality(passenger, 'Argentina')

            Utils().print_separator()


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


class Utils:
    @staticmethod
    def print_separator():
        logger.info('****************************************************')
