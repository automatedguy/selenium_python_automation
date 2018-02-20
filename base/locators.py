

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
