# coding=utf-8
import datetime
import json
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


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def wait_for_element(self, locator, description):
        self.logger.info(WAITING_FOR + description)
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(locator)
        )
        return element

    def clearing_input(self, description):
        self.logger.info(
            CLEARING + '[' + description + ']'
        )

    def print_section_tittle(self, tittle):
        self.print_separator()
        self.logger.info(tittle)
        self.print_separator()

    def filling_data(self, description, input_data):
        self.logger.info(
            FILLING + '[' + description + '] : [' + input_data + ']'
        )

    def clear_input(self, description, *locator):
        self.clearing_input(description)
        self.driver.find_element(*locator).clear()

    def fill_data(self, input_data, description, *locator):
        self.filling_data(description, input_data)
        self.driver.find_element(*locator).send_keys(input_data)
        return

    def fill_data_indexed(self, index, input_data, description, *locator):
        self.filling_data(description, input_data)
        self.driver.find_elements(*locator)[index].send_keys(input_data)
        return

    def selecting_data(self, description, option):
        self.logger.info(
            SELECTING + '[' + description + '] : [' + option + ']'
        )

    def display_selected_data(self, description, option):
        self.logger.info(
            SELECTED + '[' + description + '] : [' + option + ']'
        )

    def select_data_visible(self, option, description, *locator):
        self.selecting_data(description, option)
        Select(self.driver.find_element(*locator)).select_by_visible_text(option)
        return

    def select_data_visible_indexed(self, index, option, description, *locator):
        self.selecting_data(description, option)
        Select(self.driver.find_elements(*locator)[index]).select_by_visible_text(option)
        return

    def select_data_index_indexed(self, index, option, description, *locator):
        self.selecting_data(description, option)
        selection = Select(self.driver.find_elements(*locator)[index])
        selection.select_by_index(option)
        self.display_selected_data(description, selection.first_selected_option.text)
        return

    def clicking(self, description, button_text=None):
        self.logger.info(CLICKING + description + ' ' + button_text)

    def click_button(self, description, *locator):
        button = self.driver.find_element(*locator)
        self.clicking(description, button.text)
        button.click()

    def print_separator(self):
        self.logger.info('****************************************************')


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

    __next_button_lct = CheckoutPageLct.NEXT_BUTTON
    __next_button_desc = CheckoutPageLct.NEXT_BUTTON_DESC

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

    def save_input_definitions(self, product):
        file_path = '/home/gabrielcespedes/projects/input_definitions/'
        time_now = datetime.datetime.now()
        time_stamp = time_now.strftime("%Y%m%d-%H%M%S")
        file_name = time_stamp + '.json'
        full_path = file_path + self.country_site + '/' + product + '/' + file_name
        self.logger.info('Saving input definitions at: [' + full_path + ']')
        with open(full_path, 'w') as outfile:
            json.dump(self.input_definitions, outfile)

    def populate_sections(self, cross_selling):
        """ This method will deal with the initial load """

        self.set_input_definitions()

        filled = dict.fromkeys(["passenger_done",
                                "billing_done",
                                "contact_done",
                                "cross_selling_done",
                                "emergency_contact_done"], False)

        if not cross_selling:
            filled.update(dict.fromkeys(["cross_selling_done",
                                         "emergency_contact_done"], True))

        while not filled.get("passenger_done") or not filled.get("billing_done") or \
                not filled.get("contact_done") or not filled.get("cross_selling_done"):

            if not filled.get("cross_selling_done"):
                filled.update(dict.fromkeys(["cross_selling_done"], CrossSelling(
                    self.driver
                ).populate_cross_selling_info()))
                self.set_input_definitions()

            if not filled.get("passenger_done"):
                filled.update(dict.fromkeys(["passenger_done"], PassengerSection(
                    self.driver, self.input_definitions, self.country_site
                ).populate_passengers_info()))

            if not filled.get("emergency_contact_done"):
                filled.update(dict.fromkeys(["emergency_contact_done"], EmergencyContactSection(
                    self.driver, self.input_definitions, self.country_site
                ).populate_emergency_contact()))

            if not filled.get("billing_done"):
                filled.update(dict.fromkeys(["billing_done"], BillingSection(
                    self.driver, self.input_definitions, self.country_site
                ).populate_billing_info()))

            if not filled.get("contact_done"):
                filled.update(dict.fromkeys(["contact_done"], ContactSection(
                    self.driver, self.input_definitions, self.country_site
                ).populate_contact_info()))

            self.click_button(
                self.__next_button_desc,
                *self.__next_button_lct
            )


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
        self.logger.info(CLICKING + self.__add_insurance_desc)
        try:
            self.driver.find_elements(*self.__add_insurance_lct)[0].click()
        except WebDriverException as insurance_except:
            self.logger.warning("Trying to locate insurance radio button: [Exception]" + str(insurance_except))
            self.driver.find_elements(*self.__add_insurance_lct)[0].click()

    def populate_cross_selling_info(self):
        self.click_add_insurance()
        return True


class PassengerSection(Checkout):
    """"Passenger Section"""

    def __init__(self, driver, input_definitions, country_site):
        super(PassengerSection, self).__init__(driver)
        super(PassengerSection, self).__init__(input_definitions)
        super(PassengerSection, self).__init__(country_site)
        self.driver = driver
        self.input_definitions = input_definitions
        self.country_site = country_site
        self.document_type_options = None
        self.gender_options = None

    __first_name_lct = PassengerSectionLct.FIRST_NAME
    __first_name_desc = PassengerSectionLct.FIRST_NAME_DESC

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
    def fill_first_name(self, index, first_name=RND):
        if self.input_definitions['passengers'][index]['first_name']['required']:
            if first_name is RND:
                first_name = Utils().get_random_string(7, 10)
            self.fill_data_indexed(
                index,
                first_name,
                self.__first_name_desc,
                *self.__first_name_lct
            )

    def fill_last_name(self, index, last_name=RND):
        if self.input_definitions['passengers'][index]['last_name']['required']:
            if last_name is RND:
                last_name = Utils().get_random_string(7, 10)
            self.fill_data_indexed(
                index,
                last_name,
                self.__last_name_desc,
                *self.__last_name_lct
            )

    def get_document_type_options(self, index):
        self.document_type_options = (
            self.input_definitions['passengers'][index]['document']['document_type']['options']
        )

    def get_rand_document_type(self, index):
        self.get_document_type_options(index)
        return (
            self.document_type_options[(randint(0, len(self.document_type_options) - 1))]['description']
        )

    def select_document_type(self, index, document_type_selected=RND):
        if self.input_definitions['passengers'][index]['document']['document_type']['required']:
            if document_type_selected is RND:
                document_type_selected = self.get_rand_document_type(index)
            self.select_data_visible_indexed(
                index,
                document_type_selected,
                self.__document_type_desc,
                *self.__document_type_lct
            )

    def fill_document_number(self, index, document_number=None):
        if self.input_definitions['passengers'][index]['document']['number']['required']:
            if document_number is None:
                document_number = Utils().get_document_number(self.country_site)
            self.fill_data_indexed(
                index,
                document_number,
                self.__document_number_desc,
                *self.__document_number_lct,
            )

    def select_birthday(self, index, birthday):
        self.select_data_visible_indexed(
            index,
            birthday,
            self.__birthday_desc,
            *self.__birthday_lct
        )

    def select_birthmonth(self, index, birthmonth):
        self.select_data_index_indexed(
            index,
            birthmonth,
            self.__birthmonth_desc,
            *self.__birthmonth_lct
        )

    def select_birthyear(self, index, birthyear):
        self.select_data_visible_indexed(
            index,
            birthyear,
            self.__birthyear_desc,
            *self.__birthyear_lct
        )

    def select_birth_date(self, index):
        if self.input_definitions['passengers'][index]['birthday']['required']:
            self.select_birthday(index, str(randint(1, 28)))
            self.select_birthmonth(index, str(randint(1, 12)))
            self.select_birthyear(index, Utils().get_current_year(
                Utils().get_age(self.input_definitions['passengers'][index]['description']))
                                  )

    def get_gender_options(self, index):
        self.gender_options = (
            self.input_definitions['passengers'][index]['gender']['options']
        )

    def get_rand_gender(self, index):
        self.get_gender_options(index)
        return (
            self.gender_options[(randint(0, len(self.document_type_options) - 1))]['description']
        )

    def select_gender(self, index, gender=RND):
        if self.input_definitions['passengers'][index]['gender']['required']:
            if gender is RND:
                gender = self.get_rand_gender(index)
            self.select_data_visible_indexed(
                index,
                gender,
                self.__gender_desc,
                *self.__gender_lct
            )

    def select_nationality(self, index, nationality=None):
        if self.input_definitions['passengers'][index]['nationality']['required']:
            if nationality is None:
                nationality = Utils().get_nationality(self.country_site)
            self.select_data_visible_indexed(
                index,
                nationality,
                self.__nationality_desc,
                *self.__nationality_lct
            )

    def populate_passengers_info(self):

        self.wait_for_element(PassengerSectionLct.FIRST_NAME, PASSENGERS_SECTION)
        self.print_section_tittle(CHECKING_PASSENGERS_DISPLAYED)

        if self.driver.find_element(*self.__first_name_lct).is_displayed():
            total_passengers = len(self.driver.find_elements(*self.__first_name_lct))
            self.print_section_tittle(PASSENGERS_INFO + ' ' + str(total_passengers))

            for passenger in range(0, total_passengers):
                self.filling_data(PASSENGER_NUM, str(passenger + 1))

                self.fill_first_name(passenger)
                self.fill_last_name(passenger)
                self.select_document_type(passenger)
                self.fill_document_number(passenger)
                self.select_birth_date(passenger)
                self.select_gender(passenger)
                self.select_nationality(passenger)
                self.print_separator()
            return True

        else:
            self.logger.info(PASSENGERS_NOT_DISPLAYED)
            return False


class BillingSection(Checkout):
    """ Billing Section """

    def __init__(self, driver, input_definitions, country_site):
        super(BillingSection, self).__init__(driver)
        super(BillingSection, self).__init__(input_definitions)
        super(BillingSection, self).__init__(country_site)
        self.driver = driver
        self.input_definitions = input_definitions
        self.country_site = country_site
        self.fiscal_type_options = None
        self.states_options = None

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
    def fill_fiscal_name(self, fiscal_name):
        if self.input_definitions['billings'][0]['fiscal_name']['required']:
            self.fill_data(
                fiscal_name,
                self.__fiscal_name_desc,
                *self.__fiscal_name_lct
            )

    def get_fiscal_type_options(self):
        self.logger.info('Getting fiscal type available options from input definitions...')
        self.fiscal_type_options = self.input_definitions['billings'][0]['fiscal_type_document']['options']
        self.logger.info('Available options are:' + str(self.fiscal_type_options))

    def get_rand_fiscal_type(self):
        self.get_fiscal_type_options()
        return self.fiscal_type_options[(randint(0, len(self.fiscal_type_options) - 1))]['description']

    def select_fiscal_type(self, fiscal_type):
        if self.input_definitions['billings'][0]['fiscal_type']['required']:
            self.select_data_visible(
                fiscal_type,
                self.__fiscal_type_desc,
                *self.__fiscal_type_lct
            )

    def fill_fiscal_document(self, fiscal_document):
        if self.input_definitions['billings'][0]['fiscal_document']['required']:
            self.fill_data(
                fiscal_document,
                self.__fiscal_document_desc,
                *self.__fiscal_document_lct
            )

    def fill_address_street(self, address_street):
        if self.input_definitions['billings'][0]['address']['street']['required']:
            self.fill_data(
                address_street,
                self.__address_street_desc,
                *self.__address_street_lct
            )

    def fill_address_number(self, address_number):
        try:
            if self.input_definitions['billings'][0]['address']['number']['required']:
                self.fill_data(
                    address_number,
                    self.__address_number_desc,
                    *self.__address_number_lct
                )
        except Exception as no_address_number:
            self.logger.warning('Address number is not available [Exception]: ' + str(no_address_number))

    def fill_address_floor(self, address_floor):
        try:
            if not self.input_definitions['billings'][0]['address']['floor']['required']:
                self.fill_data(
                    address_floor,
                    self.__address_floor_desc,
                    *self.__address_floor_lct
                )
        except Exception as no_floor:
            self.logger.warning('Floor is not available [Exception]: ' + str(no_floor))

    def fill_address_department(self, address_department):
        try:
            if not self.input_definitions['billings'][0]['address']['department']['required']:
                self.fill_data(
                    address_department,
                    self.__address_department_desc,
                    *self.__address_department_lct
                )
        except Exception as no_department:
            self.logger.warning('Department is not available [Exception]: ' + str(no_department))

    def fill_address_postal_code(self, address_postal_code):
        try:
            if self.input_definitions['billings'][0]['address']['postal_code']['required']:
                self.fill_data(
                    address_postal_code,
                    self.__address_postal_code_desc,
                    *self.__address_postal_code_lct
                )
        except Exception as no_postal_code:
            self.logger.warning('Postal code is not available [Exception]: ' + str(no_postal_code))

    def get_states_options(self):
        self.states_options = self.input_definitions['billings'][0]['address']['states']['options']

    def get_rand_state(self):
        self.get_states_options()
        return self.states_options[randint(1, len(self.states_options) - 1)]['description']

    def fill_address_state(self, address_state):
        if self.input_definitions['billings'][0]['address']['states']['required']:
            self.fill_data(
                address_state,
                self.__address_state_desc,
                *self.__address_state_ltc
            )

    def fill_address_city(self, address_city):
        if self.input_definitions['billings'][0]['address']['city']['required']:
            self.fill_data(
                address_city,
                self.__address_city_desc,
                *self.__address_city_lct
            )

    def populate_billing_info(self):
        self.print_section_tittle(CHECKING_BILLING_SECTION_DISPLAYED)

        if self.driver.find_element(*self.__fiscal_name_lct).is_displayed():

            self.print_section_tittle(POPULATING_BILLING_SECTION)

            self.fill_fiscal_name('Panqueca')
            self.select_fiscal_type(self.get_rand_fiscal_type())
            self.fill_fiscal_document(Utils.get_fiscal_document(self.country_site))
            self.fill_address_street('Fake Street 123')
            self.fill_address_number('12345')
            self.fill_address_floor('10')
            self.fill_address_department('A')
            self.fill_address_postal_code(Utils().get_postal_code(self.country_site))
            self.fill_address_state(self.get_rand_state())
            self.fill_address_city(Utils().get_country_city(self.country_site))
            self.print_separator()
            return True
        else:
            self.logger.info(BILLING_SECTION_NOT_DISPLAYED)
            return False


class ContactSection(Checkout):
    """ Contact Section """

    def __init__(self, driver, input_definitions, country_site):
        super(ContactSection, self).__init__(driver)
        super(ContactSection, self).__init__(input_definitions)
        super(ContactSection, self).__init__(country_site)
        self.driver = driver
        self.input_definitions = input_definitions
        self.country_site = country_site
        self.telephone_type_options = None

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

    def fill_email(self, email):
        if self.input_definitions['contacts'][0]['email']['required']:
            self.fill_data(
                email,
                self.__email_desc,
                *self.__email_lct
            )

    def fill_email_confirmation(self, email_confirmation):
        if self.input_definitions['contacts'][0]['email']['required']:
            self.fill_data(
                email_confirmation,
                self.__email_confirmation_desc,
                *self.__email_confirmation_lct
            )

    def get_telephone_type_options(self):
        self.telephone_type_options = \
            self.input_definitions['contacts'][0]['telephones'][0]['telephone_type']['options']

    def get_rand_telephone_type(self):
        self.get_telephone_type_options()
        return self.telephone_type_options[randint(0, len(self.telephone_type_options) - 1)]['description']

    def select_telephone_type(self, telephone_type):
        self.select_data_visible(
            telephone_type,
            self.__telephone_type_desc,
            *self.__telephone_type_lct
        )

    def fill_country_code(self, country_code):
        if self.input_definitions['contacts'][0]['telephones'][0]['country_code']:
            self.clear_input(
                self.__country_code_desc,
                *self.__country_code_lct
            )
            self.fill_data(
                country_code,
                self.__country_code_desc,
                *self.__country_code_lct
            )

    def fill_area_code(self, area_code):
        if self.input_definitions['contacts'][0]['telephones'][0]['area_code']:
            self.fill_data(
                area_code,
                self.__area_code_desc,
                *self.__area_code_lct
            )

    def fill_phone_number(self, phone_number):
        if self.input_definitions['contacts'][0]['telephones'][0]['number']:
            self.fill_data(
                phone_number,
                self.__phone_number_desc,
                *self.__phone_number_lct
            )

    def populate_contact_info(self):
        self.print_section_tittle(CHECKING_CONTACTS_DISPLAYED)

        if self.driver.find_element(*self.__email_lct).is_displayed():
            self.print_section_tittle(POPULATING_CONTACT_INFO)

            self.fill_email('email@google.com')
            self.fill_email_confirmation('email@google.com')
            self.select_telephone_type(self.get_rand_telephone_type())
            self.fill_country_code(Utils().get_country_code(self.country_site))
            self.fill_area_code(Utils().get_area_code(self.country_site))
            self.fill_phone_number(Utils().get_phone_number(self.country_site))
            self.print_separator()
            return True
        else:
            self.logger.info(CONTACT_NOT_DISPLAYED)
            return False


class EmergencyContactSection(Checkout):
    """ Emergency Contact Section """

    def __init__(self, driver, input_definitions, country_site):
        super(EmergencyContactSection, self).__init__(driver)
        super(EmergencyContactSection, self).__init__(input_definitions)
        super(EmergencyContactSection, self).__init__(country_site)
        self.driver = driver
        self.input_definitions = input_definitions
        self.country_site = country_site
        self.telephone_type_options = None

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

    def fill_first_name(self, first_name):
        if self.input_definitions['emergency_contacts'][0]['first_name']['required']:
            self.fill_data(
                first_name,
                self.__first_name_desc,
                *self.__first_name_lct
            )

    def fill_last_name(self, last_name):
        if self.input_definitions['emergency_contacts'][0]['last_name']['required']:
            self.fill_data(
                last_name,
                self.__last_name_desc,
                *self.__last_name_lct
            )

    def get_telephone_type_options(self):
        self.telephone_type_options = self.input_definitions['emergency_contacts'][0]['telephone']['telephone_type'][
            'options']

    def get_rand_telephone_type(self):
        self.get_telephone_type_options()
        return self.telephone_type_options[randint(0, len(self.telephone_type_options) - 1)]['description']

    def select_telephone_type(self, telephone_type):
        self.select_data_visible(
            telephone_type,
            self.__telephone_type_desc,
            *self.__telephone_type_lct
        )

    def fill_country_code(self, country_code):
        if self.input_definitions['emergency_contacts'][0]['telephone']['country_code']['required']:
            self.fill_data(
                country_code,
                self.__country_code_desc,
                *self.__country_code_lct
            )

    def fill_area_code(self, area_code):
        if self.input_definitions['emergency_contacts'][0]['telephone']['area_code']['required']:
            self.fill_data(
                area_code,
                self.__area_code_desc,
                *self.__area_code_lct
            )

    def fill_phone_number(self, phone_number):
        if self.input_definitions['emergency_contacts'][0]['telephone']['number']['required']:
            self.fill_data(
                phone_number,
                self.__phone_number_desc,
                *self.__phone_number_lct
            )

    def populate_emergency_contact(self):
        self.print_section_tittle(CHECKING_EMERGENCY_CONTACTS_DISPLAYED)

        if self.driver.find_element(*self.__first_name_lct).is_displayed():
            self.print_section_tittle(POPULATING_EMERGENCY_CONTACT_INFO)

            self.fill_first_name(Utils().get_random_string(7, 10))
            self.fill_last_name(Utils().get_random_string(7, 10))
            self.select_telephone_type(self.get_rand_telephone_type())
            self.fill_country_code(Utils().get_country_code(self.country_site))
            self.fill_area_code(Utils().get_area_code(self.country_site))
            self.fill_phone_number(Utils().get_phone_number(self.country_site))
            self.print_separator()
            return True
        else:
            self.logger.info(EMERGENCY_CONTACT_NOT_DISPLAYED)
            return False
        return True


class PaymentSectionGrid(Checkout):
    """Payment Section Grid"""

    def __init__(self, driver):
        super(PaymentSectionGrid, self).__init__(driver)
        self.driver = driver


class PaymentSectionCombo(Checkout):
    """Payment Section Combo"""

    def __init__(self, driver):
        super(PaymentSectionCombo, self).__init__(driver)
        self.driver = driver


class PaymentSectionTwoCards(Checkout):
    """Payment Section Two Cards"""

    def __init__(self, driver):
        super(PaymentSectionTwoCards, self).__init__(driver)
        self.driver = driver


class PaymentSectionRetailCard(Checkout):
    """Payment Section Retail Card"""

    def __init__(self, driver):
        super(PaymentSectionRetailCard, self).__init__(driver)
        self.driver = driver


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
        self.logger.info(CLICKING + LoginModalLct.CLOSE_BUTTON_DESC)
        self.driver.find_element(*LoginModalLct.CLOSE_BUTTON).click()


class Utils:
    """ Utils class: all static methods for general pourposes """

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
            COL: '800999333',
            MEX: '28549400',
            BRA: '12345678900'
        }
        document_number.get(country_site, 'Invalid country' + country_site)
        return document_number.get(country_site)

    @staticmethod
    def get_document_number_exp(country_site):
        document_number = {
            'DNI': '28549400',
            'Pasaporte': '800999300',
            'CPF': '28549400',
            'NIT': '12345678900',
            '': '',
            '': ''

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

    @staticmethod
    def get_fiscal_document(country_site):
        fiscal_document = {
            ARG: '23281685589',
            COL: '800999333',
            MEX: '28549400',
            BRA: '12345678900'
        }
        return fiscal_document.get(country_site)

    @staticmethod
    def get_country_city(country_site):
        country_city = {
            ARG: 'Buenos Aires',
            COL: 'Bogota',
            MEX: 'Distrito Federal D.F.',
            BRA: 'São Paulo'
        }
        return country_city.get(country_site)

    @staticmethod
    def get_nationality(country_site):
        nationality = {
            ARG: ARGENTINA,
            COL: COLOMBIA,
            MEX: MEXICO,
            BRA: BRASIL
        }
        return nationality.get(country_site)

    @staticmethod
    def get_area_code(country_site):
        area_code = {
            ARG: '51',
            COL: '57',
            MEX: '52',
            BRA: '55'
        }
        return area_code.get(country_site)

    @staticmethod
    def get_country_code(country_site):
        country_code = {
            ARG: '11',
            COL: '111',
            MEX: '52',
            BRA: '55'
        }
        return country_code.get(country_site)

    @staticmethod
    def get_phone_number(country_site):
        phone_number = {
            ARG: '45678765',
            COL: '45678765',
            MEX: '45678765',
            BRA: '45678765'
        }
        return phone_number.get(country_site)
