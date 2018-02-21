# coding=utf-8
import logging
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from constants import *
from locators import *
from services import InputDefinitions

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

    def __init__(self, driver, cart_id=''):
        super(Checkout, self).__init__(driver)
        self.driver = driver
        self.cart_id = cart_id

    def populate_checkout_info(self, cart_id='', country='', language='', apikey=''):
        """ This method will deal with the initial load """

        # Retrieve input definitions
        input_definitions = InputDefinitions(APIST_ALMUNDO_COM, cart_id, country, language)\
            .get_input_definitions(apikey)

        # Populate the different sections
        PassengerSection(self.driver).populate_passengers_info(input_definitions)
        BillingSection(self.driver).populate_billing_info(input_definitions)
        ContactSection(self.driver).populate_contact_info(input_definitions)


class PassengerSection(Checkout):
    """"Passenger Section"""

    def __init__(self, driver):
        super(PassengerSection, self).__init__(driver)
        self.driver = driver

    # Locators
    __name_lct = PassengerSectionLct.NAME
    __name_desc = PassengerSectionLct.NAME_DESC

    __last_name_lct = PassengerSectionLct.LAST_NAME
    __last_name_desc = PassengerSectionLct.LAST_NAME_DESC

    __document_type_lct = PassengerSectionLct.DOCUMENT_TYPE
    __document_type_desc = PassengerSectionLct.DOCUMENT_TYPE_DESC

    __document_number_lct = PassengerSectionLct.DOCUMENT_NUMBER
    __document_number_desc = PassengerSectionLct.DOCUMENT_NUMBER_DESC

    __birthday_lct = PassengerSectionLct.BIRTHDAY
    __birthday_desc = PassengerSectionLct.BIRTHDAY_DESC

    __birthmonth_lct = PassengerSectionLct.BIRTHMONTH
    __birthmonth_desc = PassengerSectionLct.BIRTHMONTH_DESC

    __birthyear_lct = PassengerSectionLct.BIRTHYEAR
    __birthyear_desc = PassengerSectionLct.BIRTHYEAR_DESC

    __gender_lct = PassengerSectionLct.GENDER
    __gender_desc = PassengerSectionLct.GENDER_DESC

    __nationality_lct = PassengerSectionLct.NATIONALITY
    __nationality_desc = PassengerSectionLct.NATIONALITY_DESC

    # Actions
    def set_name(self, passenger_index, passenger_name):
        logger.info(FILLING + self.__name_desc + passenger_name)
        self.driver.find_elements(*self.__name_lct)[passenger_index].send_keys(passenger_name)

    def set_last_name(self, passenger_index, passenger_last_name):
        logger.info(FILLING + self.__last_name_desc + passenger_last_name)
        self.driver.find_elements(*self.__last_name_lct)[passenger_index].send_keys(passenger_last_name)

    def set_document_type(self, passenger_index, passenger_document_type):
        logger.info(SELECTING + self.__document_type_desc + passenger_document_type)
        Select(self.driver.find_elements(*self.__document_type_lct)[passenger_index])\
            .select_by_visible_text(passenger_document_type)

    def set_document_number(self, passenger_index, passenger_document_number):
        logger.info(FILLING + self.__document_number_desc + passenger_document_number)
        self.driver.find_elements(*self.__document_number_lct)[passenger_index].send_keys(passenger_document_number)

    def select_birthday(self, passenger_index, passenger_birthday):
        logger.info(SELECTING + self.__birthday_desc + passenger_birthday)
        Select(self.driver.find_elements(*self.__birthday_lct)[passenger_index])\
            .select_by_visible_text(passenger_birthday)

    def select_birthmonth(self, passenger_index, passenger_birthmonth):
        logger.info(SELECTING + self.__birthmonth_desc + passenger_birthmonth)
        Select(self.driver.find_elements(*self.__birthmonth_lct)[passenger_index])\
            .select_by_visible_text(passenger_birthmonth)

    def select_birthyear(self, passenger_index, passenger_birthyear):
        logger.info(SELECTING + self.__birthyear_desc + passenger_birthyear)
        Select(self.driver.find_elements(*self.__birthyear_lct)[passenger_index])\
            .select_by_visible_text(passenger_birthyear)

    def select_gender(self, passenger_index, passenger_gender):
        logger.info(SELECTING + self.__gender_desc + passenger_gender)
        Select(self.driver.find_elements(*self.__gender_lct)[passenger_index])\
            .select_by_visible_text(passenger_gender)

    def select_nationality(self, passenger_index, passenger_nationality):
        logger.info(SELECTING + self.__nationality_desc + passenger_nationality)
        Select(self.driver.find_elements(*self.__nationality_lct)[passenger_index])\
            .select_by_visible_text(passenger_nationality)

    def populate_passengers_info(self, input_definitions):

        total_passengers = len(self.driver.find_elements(*PassengerSectionLct.NAME))

        Utils().print_separator()
        logger.info("Filling Passengers info - Total Passengers: " + str(total_passengers))
        Utils().print_separator()

        for passenger in range(0, total_passengers):
            logger.info('Filling Passenger N°: ' + str(passenger + 1))

            if input_definitions['passengers'][passenger]['first_name']['required']:
                self.set_name(passenger, 'Whatever')

            if input_definitions['passengers'][passenger]['last_name']['required']:
                self.set_last_name(passenger, 'Nevermind')

            if input_definitions['passengers'][passenger]['document']['document_type']['required']:
                self.set_document_type(passenger, 'Pasaporte')

            if input_definitions['passengers'][passenger]['document']['number']['required']:
                self.set_document_number(passenger, '23456543N')

            if input_definitions['passengers'][passenger]['birthday']['required']:
                self.select_birthday(passenger, '1')
                self.select_birthmonth(passenger, 'Enero')
                self.select_birthyear(passenger, '1990')

            if input_definitions['passengers'][passenger]['gender']['required']:
                self.select_gender(passenger, 'Masculino')

            if input_definitions['passengers'][passenger]['nationality']['required']:
                self.select_nationality(passenger, 'Argentina')

            Utils().print_separator()


class BillingSection(Checkout):
    """ Billing Section """

    def __init__(self, driver):
        super(BillingSection, self).__init__(driver)
        self.driver = driver

    # Locators

    __fiscal_name_lct = BillingSectionLct.FISCAL_NAME
    __fiscal_name_desc = BillingSectionLct.FISCAL_NAME_DESC

    __fiscal_type_lct = BillingSectionLct.FISCAL_TYPE
    __fiscal_type_desc = BillingSectionLct.FISCAL_TYPE_DESC

    __fiscal_document_lct = BillingSectionLct.FISCAL_DOCUMENT
    __fiscal_document_desc = BillingSectionLct.FISCAL_DOCUMENT_DESC

    __address_street_lct = BillingSectionLct.ADDRESS_STREET
    __address_street_desc = BillingSectionLct.ADDRESS_STREET_DESC

    __address_number_lct = BillingSectionLct.ADDRESS_NUMBER
    __address_number_desc = BillingSectionLct.ADDRESS_NUMBER_DESC

    __address_floor_lct = BillingSectionLct.ADDRESS_FLOOR
    __address_floor_desc = BillingSectionLct.ADDRESS_FLOOR_DESC

    __address_department_lct = BillingSectionLct.ADDRESS_DEPARTMENT
    __address_department_desc = BillingSectionLct.ADDRESS_DEPARTMENT_DESC

    __address_postal_code_lct = BillingSectionLct.ADDRESS_POSTAL_CODE
    __address_postal_code_desc = BillingSectionLct.ADDRESS_POSTAL_CODE_DESC

    __address_state_ltc = BillingSectionLct.ADDRESS_STATE
    __address_state_desc = BillingSectionLct.ADDRESS_STATE_DESC

    __address_city_lct = BillingSectionLct.ADDRESS_CITY
    __address_city_desc = BillingSectionLct.ADDRESS_CITY_DESC

    __enable_billing_lct = BillingSectionLct.ENABLE_BILLING
    __enable_billing_desc = BillingSectionLct.ENABLE_BILLING_DESC

    # Actions:
    def set_fiscal_name(self, billing_fiscal_name):
        logger.info(FILLING + self.__fiscal_name_desc + billing_fiscal_name)
        self.driver.find_element(*self.__fiscal_name_lct).send_keys(billing_fiscal_name)

    def select_fiscal_type(self, billing_fiscal_type):
        logger.info(SELECTING + self.__fiscal_type_desc + billing_fiscal_type)
        Select(self.driver.find_element(*self.__fiscal_type_lct)).select_by_visible_text(billing_fiscal_type)

    def set_fiscal_document(self, billing_fiscal_document):
        logger.info(FILLING + self.__fiscal_document_desc + billing_fiscal_document)
        self.driver.find_element(*self.__fiscal_document_lct).send_keys(billing_fiscal_document)

    def set_address_street(self, billing_address_street):
        logger.info(FILLING + self.__address_street_desc + billing_address_street)
        self.driver.find_element(*self.__address_street_lct).send_keys(billing_address_street)

    def set_address_number(self, billing_address_number):
        logger.info(FILLING + self.__address_number_desc + billing_address_number)
        self.driver.find_element(*self.__address_number_lct).send_keys(billing_address_number)

    def set_address_floor(self, billing_address_floor):
        logger.info(FILLING + self.__address_floor_desc + billing_address_floor)
        self.driver.find_element(*self.__address_floor_lct).send_keys(billing_address_floor)

    def set_address_department(self, billing_address_department):
        logger.info(FILLING + self.__address_department_desc + billing_address_department)
        self.driver.find_element(*self.__address_department_lct).send_keys(billing_address_department)

    def set_address_postal_code(self, billing_address_postal_code):
        logger.info(FILLING + self.__address_postal_code_desc + billing_address_postal_code)
        self.driver.find_element(*self.__address_postal_code_lct).send_keys(billing_address_postal_code)

    def set_address_state(self, billing_address_state):
        logger.info(FILLING + self.__address_state_desc + billing_address_state)
        self.driver.find_element(*self.__address_state_ltc).send_keys(billing_address_state)

    def set_address_city(self, billing_address_city):
        logger.info(FILLING + self.__address_city_desc + billing_address_city)
        self.driver.find_element(*self.__address_city_lct).send_keys(billing_address_city)

    def populate_billing_info(self, input_definitions):
        logger.info("Populating Billing Info")
        Utils().print_separator()

        if input_definitions['billings'][0]['fiscal_name']['required']:
            self.set_fiscal_name('Saraza')

        if input_definitions['billings'][0]['fiscal_type']['required']:
            self.select_fiscal_type('Consumidor Final')

        if input_definitions['billings'][0]['fiscal_document']['required']:
            self.set_fiscal_document('23281685589')

        if input_definitions['billings'][0]['address']['street']['required']:
            self.set_address_street('Fake Street 123')

        if input_definitions['billings'][0]['address']['number']['required']:
            self.set_address_number('12345')
            self.set_address_floor('10')
            self.set_address_department('A')

        if input_definitions['billings'][0]['address']['postal_code']['required']:
            self.set_address_postal_code('7777')

        if input_definitions['billings'][0]['address']['states']['required']:
            self.set_address_state('Ciudad Autónoma de Buenos Aires')

        if input_definitions['billings'][0]['address']['city']['required']:
            self.set_address_city('Buenos Aires')

        Utils().print_separator()


class ContactSection(Checkout):
    """ Contact Section """

    def __init__(self, driver):
        super(ContactSection, self).__init__(driver)
        self.driver = driver

    __email_lct = ContactSectionLct.EMAIL
    __email_desc = ContactSectionLct.EMAIL_DESC

    __email_confirmation_lct = ContactSectionLct.EMAIL_CONFIRMATION
    __email_confirmation_desc = ContactSectionLct.EMAIL_CONFIRMATION_DESC

    __telephone_type_lct = ContactSectionLct.TELEPHONE_TYPE
    __telephone_type_desc = ContactSectionLct.TELEPHONE_TYPE_DESC

    __country_code_lct = ContactSectionLct.COUNTRY_CODE
    __country_code_desc = ContactSectionLct.COUNTRY_CODE_DESC

    __area_code_lct = ContactSectionLct.AREA_CODE
    __area_code_desc = ContactSectionLct.AREA_CODE_DESC

    __phone_number_lct = ContactSectionLct.PHONE_NUMBER
    __phone_number_desc = ContactSectionLct.PHONE_NUMBER_DESC

    def set_email(self, contact_email):
        logger.info(FILLING + self.__email_desc + contact_email)
        self.driver.find_element(*self.__email_lct).send_keys(contact_email)

    def set_email_confirmation(self, contact_email_confirmation):
        logger.info(FILLING + self.__email_confirmation_desc + contact_email_confirmation)
        self.driver.find_element(*self.__email_confirmation_lct).send_keys(contact_email_confirmation)

    def select_telephone_type(self, contact_telephone_type):
        logger.info(FILLING + self.__telephone_type_desc + contact_telephone_type)
        self.driver.find_element(*self.__telephone_type_lct).send_keys(contact_telephone_type)

    def set_country_code(self, contact_country_code):
        logger.info(FILLING + self.__country_code_desc + contact_country_code)
        self.driver.find_element(*self.__country_code_lct).send_keys(contact_country_code)

    def set_area_code(self, contact_area_code):
        logger.info(FILLING + self.__area_code_desc + contact_area_code)
        self.driver.find_element(*self.__area_code_lct).send_keys(contact_area_code)

    def set_phone_number(self, contact_phone_number):
        logger.info(FILLING + self.__phone_number + contact_phone_number)
        self.driver.find_element(*self.__phone_number).send_keys(contact_phone_number)

    def populate_contact_info(self, input_definitions):
        logger.info("Populating Contact Info")
        Utils().print_separator()

        if input_definitions['contacts'][0]['email']['required']:
            self.set_email('email@google.com')
            self.set_email_confirmation('email@google.com')

        self.select_telephone_type('Celular')

        if input_definitions['contacts'][0]['telephones'][0]['country_code']:
            self.set_country_code('54')

        if input_definitions['contacts'][0]['telephones'][0]['area_code']:
            self.set_area_code('11')

        if input_definitions['contacts'][0]['telephones'][0]['number']:
            self.set_phone_number('43527685')

        Utils().print_separator()


class EmergencyContactSection:
    """ Emergency Contact Section """

    def __init__(self, driver):
        super(EmergencyContactSection, self).__init__(driver)
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
        logger.info(CLICKING + LoginModalLct.CLOSE_BUTTON_DESC)
        self.driver.find_element(*LoginModalLct.CLOSE_BUTTON).click()


class Utils:
    @staticmethod
    def print_separator():
        logger.info('****************************************************')
