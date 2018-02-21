

from selenium.webdriver.common.by import By


class LoginModalLct(object):

    CLOSE_BUTTON = (By.CSS_SELECTOR, '#section .header-modal span')
    CLOSE_BUTTON_DESC = 'Close login modal (X)'


class PassengerSectionLct(object):
    NAME = (By.CSS_SELECTOR, '#first_name')
    NAME_DESC = 'Name: '

    LAST_NAME = (By.CSS_SELECTOR, '#last_name')
    LAST_NAME_DESC = 'Last Name: '

    DOCUMENT_TYPE = (By.CSS_SELECTOR, 'passengers-form #document_type')
    DOCUMENT_TYPE_DESC = 'Document Type: '

    DOCUMENT_NUMBER = (By.CSS_SELECTOR, 'passengers-form #number')
    DOCUMENT_NUMBER_DESC = 'Document Number: '

    DOCUMENT_EMISOR = (By.ID, 'document_emisor')
    DOCUMENT_EMISOR_DESC = 'Document Emisor: '

    BIRTHDAY = (By.CSS_SELECTOR, '#passengers-section passengers-form .container-day select')
    BIRTHDAY_DESC = 'Birth date [Day]: '

    BIRTHMONTH = (By.CSS_SELECTOR, '#passengers-section passengers-form .container-month select')
    BIRTHMONTH_DESC = 'Birth date [Month]: '

    BIRTHYEAR = (By.CSS_SELECTOR, '#passengers-section passengers-form .container-year select')
    BIRTHYEAR_DESC = 'Birth date [Year]: '

    GENDER = (By.ID, 'gender')
    GENDER_DESC = 'Gender: '

    NATIONALITY = (By.ID, 'nationality')
    NATIONALITY_DESC = 'Nationality: '


class BillingSectionLct(object):
    FISCAL_NAME = (By.ID, 'fiscal_name')
    FISCAL_NAME_DESC = 'Fiscal name: '

    FISCAL_TYPE = (By.ID, 'fiscal_type')
    FISCAL_TYPE_DESC = 'Fiscal type: '

    FISCAL_DOCUMENT = (By.ID, 'fiscal_document')
    FISCAL_DOCUMENT_DESC = 'Fiscal document: '

    ADDRESS_STREET = (By.ID, 'street')
    ADDRESS_STREET_DESC = 'Address street: '

    ADDRESS_NUMBER = (By.CSS_SELECTOR, 'billing-form #number')
    ADDRESS_NUMBER_DESC = 'Address number: '

    ADDRESS_FLOOR = (By.ID, 'floor')
    ADDRESS_FLOOR_DESC = 'Address floor: '

    ADDRESS_DEPARTMENT = (By.ID, 'department')
    ADDRESS_DEPARTMENT_DESC = 'Address department: '

    ADDRESS_POSTAL_CODE = (By.ID, 'postal_code')
    ADDRESS_POSTAL_CODE_DESC = 'Address postal code: '

    ADDRESS_STATE = (By.ID, 'state')
    ADDRESS_STATE_DESC = 'Address state: '

    ADDRESS_CITY = (By.ID, 'city')
    ADDRESS_CITY_DESC = 'Address city: '

    ENABLE_BILLING = (By.CSS_SELECTOR, 'billing-section div:nth-child(2) > input')
    ENABLE_BILLING_DESC = 'Enable billing radio button'
