# coding=utf-8
import datetime
import logging
import string

from selenium.common.exceptions import WebDriverException

from base.locators import *
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from random import randint, choice

from base.constants import *
from services import Apikeys, InputDefinitions

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, description):
        logger.info('Waiting for: [' + description + ']')
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        return element

# Checkout class and sections


class Checkout(BasePage):
    """Checkout Page class"""

    def __init__(self, driver, cart_id='', channel='', api_host='', country_site='', country_language=''):
        super(Checkout, self).__init__(driver)
        self.driver = driver
        self.cart_id = cart_id
        self.channel = channel
        self.api_host = api_host
        self.country_site = country_site
        self.country_language = country_language
        self.input_definitions = None

    def set_input_definitions(self):
        self.input_definitions = InputDefinitions(
            self.api_host,
            self.cart_id,
            self.country_site,
            self.country_language
        ).get_input_definitions(
            Apikeys().get_apikey(
                self.channel
            )
        )

    def populate_checkout_info(self, add_cross_selling):
        """ This method will deal with the initial load """

        # Get the input definitions for the first time
        self.set_input_definitions()

        # Come on!! Get this from the input definitions!!
        # and that will be better.
        passenger_done = False
        billing_done = False
        contact_done = False
        cross_selling_done = False
        emergency_contact_done = False

        if not add_cross_selling:
            cross_selling_done = True
            emergency_contact_done = True

        # Populate the different sections iterating and trying
        while not passenger_done or not billing_done or not contact_done or not cross_selling_done:

            if not cross_selling_done:
                cross_selling_done = CrossSelling(
                    self.driver).populate_cross_selling_info()
                self.set_input_definitions()

            if not passenger_done:
                passenger_done = PassengerSection(
                    self.driver, self.country_site).populate_passengers_info(
                    self.input_definitions
                )

            if not emergency_contact_done:
                emergency_contact_done = EmergencyContactSection(
                    self.driver).populate_emergency_contact(
                    self.input_definitions
                )

            if not billing_done:
                billing_done = BillingSection(
                    self.driver, self.country_site).populate_billing_info(
                    self.input_definitions
                )

            if not contact_done:
                contact_done = ContactSection(
                    self.driver).populate_contact_info(
                    self.input_definitions
                )

            # TODO: do something decent with this line below i.e define next button :)
            self.driver.find_element(By.CSS_SELECTOR, '.am-wizard-footer button.button-next').click()


class CrossSelling(Checkout):
    """Cross Selling section"""

    def __init__(self, driver):
        super(CrossSelling, self).__init__(driver)
        self.driver = driver

    # Locators
    __add_insurance_lct = CrossSellingSectionLct.ADD_INSURANCE
    __add_insurance_desc = CrossSellingSectionLct.ADD_INSURANCE_DESC

    __add_transfer_lct = CrossSellingSectionLct.ADD_TRANSFER
    __add_transfer_desc = CrossSellingSectionLct.ADD_INSURANCE_DESC

    def click_add_insurance(self):
        logger.info(CLICKING + self.__add_insurance_desc)
        try:
            self.driver.find_elements(*self.__add_insurance_lct)[0].click()
        except WebDriverException as insurance_except:
            logger.warning("Trying to locate insurance radio button: [Exception]" + str(insurance_except))
            self.driver.find_elements(*self.__add_insurance_lct)[0].click()

    def populate_cross_selling_info(self):
        self.click_add_insurance()
        return True


class PassengerSection(Checkout):
    """"Passenger Section"""

    def __init__(self, driver, country_site):
        super(PassengerSection, self).__init__(driver)
        super(PassengerSection, self).__init__(country_site)
        self.driver = driver
        self.country_site = country_site
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
    def set_name(self, passenger_index):
        passenger_name = Utils().get_random_string(7, 10)
        logger.info(FILLING + self.__name_desc + passenger_name)
        self.driver.find_elements(*self.__name_lct)[passenger_index].send_keys(passenger_name)

    def set_last_name(self, passenger_index):
        passenger_last_name = Utils().get_random_string(7, 10)
        logger.info(FILLING + self.__last_name_desc + passenger_last_name)
        self.driver.find_elements(*self.__last_name_lct)[passenger_index].send_keys(passenger_last_name)

    def set_document_type(self, passenger_index, document_type_options):
        document_type_selected = document_type_options[(randint(0, len(document_type_options) - 1))]['description']
        logger.info(SELECTING + self.__document_type_desc + document_type_selected)
        Select(self.driver.find_elements(*self.__document_type_lct)[passenger_index]) \
            .select_by_visible_text(document_type_selected)

    def set_document_number(self, passenger_index, passenger_document_number):
        logger.info(FILLING + self.__document_number_desc + passenger_document_number)
        self.driver.find_elements(*self.__document_number_lct)[passenger_index].send_keys(passenger_document_number)

    def select_birthday(self, passenger_index):
        passenger_birthday = str(randint(1, 28))
        logger.info(SELECTING + self.__birthday_desc + passenger_birthday)
        Select(self.driver.find_elements(*self.__birthday_lct)[passenger_index]) \
            .select_by_visible_text(passenger_birthday)

    def select_birthmonth(self, passenger_index):
        passenger_birthmonth = str(randint(1, 12))
        logger.info(SELECTING + self.__birthmonth_desc + passenger_birthmonth)
        Select(self.driver.find_elements(*self.__birthmonth_lct)[passenger_index]) \
            .select_by_index(passenger_birthmonth)

    def select_birthyear(self, passenger_index, passenger_age_range):
        passenger_birthyear = Utils().get_current_year(Utils().get_age(passenger_age_range))

        logger.info(SELECTING + self.__birthyear_desc + passenger_birthyear)
        Select(self.driver.find_elements(*self.__birthyear_lct)[passenger_index]) \
            .select_by_visible_text(passenger_birthyear)

    def select_gender(self, passenger_index, passenger_gender):
        logger.info(SELECTING + self.__gender_desc + passenger_gender)
        Select(self.driver.find_elements(*self.__gender_lct)[passenger_index]) \
            .select_by_visible_text(passenger_gender)

    def select_nationality(self, passenger_index, passenger_nationality):
        logger.info(SELECTING + self.__nationality_desc + passenger_nationality)
        Select(self.driver.find_elements(*self.__nationality_lct)[passenger_index]) \
            .select_by_visible_text(passenger_nationality)

    def populate_passengers_info(self, input_definitions):

        self.wait_for_element(PassengerSectionLct.NAME, 'Passenger first name fields')

        logger.info('Checking if Passengers section is displayed')
        if self.driver.find_element(*self.__name_lct).is_displayed():
            total_passengers = len(self.driver.find_elements(*self.__name_lct))

            Utils().print_separator()
            logger.info("Filling Passengers info - Total Passengers: " + str(total_passengers))
            Utils().print_separator()

            for passenger in range(0, total_passengers):
                logger.info('Filling Passenger N°: ' + str(passenger + 1))

                if input_definitions['passengers'][passenger]['first_name']['required']:
                    self.set_name(passenger)

                if input_definitions['passengers'][passenger]['last_name']['required']:
                    self.set_last_name(passenger)

                if input_definitions['passengers'][passenger]['document']['document_type']['required']:
                    options = input_definitions['passengers'][passenger]['document']['document_type']['options']
                    self.set_document_type(passenger, options)

                if input_definitions['passengers'][passenger]['document']['number']['required']:
                    self.set_document_number(passenger, Utils().get_document_number(self.country_site))

                if input_definitions['passengers'][passenger]['birthday']['required']:
                    self.select_birthday(passenger)
                    self.select_birthmonth(passenger)
                    age_range = input_definitions['passengers'][passenger]['description']
                    self.select_birthyear(passenger, age_range)

                if input_definitions['passengers'][passenger]['gender']['required']:
                    self.select_gender(passenger, 'Masculino')

                if input_definitions['passengers'][passenger]['nationality']['required']:
                    self.select_nationality(passenger, 'Argentina')

                Utils().print_separator()
            return True
        else:
            logger.info('Passengers section is not displayed.')
            return False


class BillingSection(Checkout):
    """ Billing Section """

    def __init__(self, driver, country_site):
        super(BillingSection, self).__init__(driver)
        super(BillingSection, self).__init__(country_site)
        self.driver = driver
        self.country_site = country_site

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

    def select_fiscal_type(self, options):
        billing_fiscal_type = options[(randint(0, len(options) - 1))]['description']
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

    def set_address_state(self, options):
        billing_address_state = options[randint(1, len(options) - 1)]['description']
        logger.info(FILLING + self.__address_state_desc + billing_address_state)
        self.driver.find_element(*self.__address_state_ltc).send_keys(billing_address_state)

    def set_address_city(self, billing_address_city):
        logger.info(FILLING + self.__address_city_desc + billing_address_city)
        self.driver.find_element(*self.__address_city_lct).send_keys(billing_address_city)

    def populate_billing_info(self, input_definitions):
        logger.info('Checking if Billing section is displayed')

        if self.driver.find_element(*self.__fiscal_name_lct).is_displayed():

            logger.info("Populating Billing Info")
            Utils().print_separator()

            if input_definitions['billings'][0]['fiscal_name']['required']:
                self.set_fiscal_name('Saraza')

            if input_definitions['billings'][0]['fiscal_type']['required']:
                options = input_definitions['billings'][0]['fiscal_type_document']['options']
                self.select_fiscal_type(options)

            if input_definitions['billings'][0]['fiscal_document']['required']:
                self.set_fiscal_document('23281685589')

            if input_definitions['billings'][0]['address']['street']['required']:
                self.set_address_street('Fake Street 123')

            if input_definitions['billings'][0]['address']['number']['required']:
                self.set_address_number('12345')

            try:
                if not input_definitions['billings'][0]['address']['floor']['required']:
                    self.set_address_floor('10')
            except Exception as no_floor:
                logger.warning('Floor is not available [Exception]: ' + str(no_floor))

            try:
                if not input_definitions['billings'][0]['address']['department']['required']:
                    self.set_address_department('A')
            except Exception as no_department:
                logger.warning('Department is not available [Exception]: ' + str(no_department))

            if input_definitions['billings'][0]['address']['postal_code']['required']:
                self.set_address_postal_code(Utils().get_postal_code(self.country_site))

            if input_definitions['billings'][0]['address']['states']['required']:
                options = input_definitions['billings'][0]['address']['states']['options']
                self.set_address_state(options)

            if input_definitions['billings'][0]['address']['city']['required']:
                self.set_address_city('Buenos Aires')

            Utils().print_separator()
            return True
        else:
            logger.info('Billing section is not displayed.')
            return False


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

    def select_telephone_type(self, contact_telephone_type_options):
        contact_telephone_type = contact_telephone_type_options[randint(0, len(contact_telephone_type_options) - 1)][
            'description']
        logger.info(FILLING + self.__telephone_type_desc + contact_telephone_type)
        self.driver.find_element(*self.__telephone_type_lct).send_keys(contact_telephone_type)

    def set_country_code(self, contact_country_code):
        logger.info(FILLING + self.__country_code_desc + contact_country_code)
        country_code = self.driver.find_element(*self.__country_code_lct)
        country_code.clear()
        country_code.send_keys(contact_country_code)

    def set_area_code(self, contact_area_code):
        logger.info(FILLING + self.__area_code_desc + contact_area_code)
        self.driver.find_element(*self.__area_code_lct).send_keys(contact_area_code)

    def set_phone_number(self, contact_phone_number):
        logger.info(FILLING + self.__phone_number_desc + contact_phone_number)
        self.driver.find_element(*self.__phone_number_lct).send_keys(contact_phone_number)

    def populate_contact_info(self, input_definitions):
        logger.info('Checking if contact section is displayed')
        if self.driver.find_element(*self.__email_lct).is_displayed():
            logger.info("Populating Contact Info")
            Utils().print_separator()

            if input_definitions['contacts'][0]['email']['required']:
                self.set_email('email@google.com')
                self.set_email_confirmation('email@google.com')

            telephone_type_options = input_definitions['contacts'][0]['telephones'][0]['telephone_type']['options']
            self.select_telephone_type(telephone_type_options)

            if input_definitions['contacts'][0]['telephones'][0]['country_code']:
                self.set_country_code('54')

            if input_definitions['contacts'][0]['telephones'][0]['area_code']:
                self.set_area_code('11')

            if input_definitions['contacts'][0]['telephones'][0]['number']:
                self.set_phone_number('43527685')

            Utils().print_separator()
            return True
        else:
            logger.info('Contact section is not displayed.')
            return False


class EmergencyContactSection:
    """ Emergency Contact Section """

    def __init__(self, driver):
        super(EmergencyContactSection, self).__init__(driver)
        self.driver = driver

    __first_name_lct = EmergencyContactSection.FIRST_NAME
    __first_name_desc = EmergencyContactSection.FIRST_NAME_DESC

    __last_name_lct = EmergencyContactSection.LAST_NAME
    __last_name_desc = EmergencyContactSection.LAST_NAME_DESC

    __telephone_type_lct = EmergencyContactSection.TELEPHONE_TYPE
    __telephone_type_desc = EmergencyContactSection.TELEPHONE_TYPE_DESC

    __country_code_lct = EmergencyContactSection.COUNTRY_CODE
    __country_code_desc = EmergencyContactSection.COUNTRY_CODE_DESC

    __area_code_lct = EmergencyContactSection.AREA_CODE
    __area_code_desc = EmergencyContactSection.AREA_CODE_DESC

    __phone_number_lct = EmergencyContactSection.PHONE_NUMBER
    __phone_number_desc = EmergencyContactSection.PHONE_NUMBER_DESC

    def set_first_name(self, emergency_contact_first_name):
        logger.info(FILLING + self.__first_name_desc + emergency_contact_first_name)
        self.driver.find_element(*self.__first_name_lct).send_keys(emergency_contact_first_name)

    def set_last_name(self, emergency_contact_last_name):
        logger.info(FILLING + self.__last_name_desc + emergency_contact_last_name)
        self.driver.find_element(*self.__last_name_lct).send_keys(emergency_contact_last_name)

    def set_telephone_type(self):
        logger.info(SELECTING + self.__telephone_type_desc)
        Select(self.driver.find_element(*self.__telephone_type_lct)).select_by_visible_text()

    def populate_emergency_contact(self, input_definitions):
        return True


class PaymentSection(Checkout):
    """Payment Section"""

    def __init__(self, driver):
        super(PaymentSection, self).__init__(driver)
        self.driver = driver

    def populate_grid(self):
        return

    def populate_combo(self):
        return

    def populate_card_info(self):
        return

    def populate_credit_card_retail(self):
        return


class AgentSection(Checkout):
    """ Agent Section"""

    def __init__(self, driver):
        super(AgentSection, self).__init__(driver)
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
    """ Utils class: all static methods for general pourposes """

    @staticmethod
    def print_separator():
        logger.info('****************************************************')

    @staticmethod
    def get_current_year(remove_years):
        time_now = datetime.datetime.now()
        new_time = time_now + datetime.timedelta(remove_years * 365)
        return new_time.strftime("%Y")

    @staticmethod
    def get_postal_code(country_site):
        postal_code = {
            ARG: '1009',
            COL: '110111',
            MEX: '03400',
            BRA: '20000-000'
        }
        postal_code.get(country_site, 'Invalid country' + country_site)
        return postal_code.get(country_site)

    @staticmethod
    def get_document_number(country_site):
        document_number = {
            ARG: '28549400',
            COL: '28549400',
            MEX: '28549400',
            BRA: '12345678900'
        }
        document_number.get(country_site, 'Invalid country' + country_site)
        return document_number.get(country_site)

    @staticmethod
    def get_age(age_range):
        age = {
            'ADULT': -13,
            'CHILD': -7,
            'INFANT': -1,
        }
        age.get(age_range, 'Invalid age range' + age_range)
        return age.get(age_range)

    @staticmethod
    def get_random_string(min_char, max_char):
        all_char = string.ascii_letters
        return "".join(choice(all_char) for x in range(randint(min_char, max_char)))
