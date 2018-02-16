

from selenium.webdriver.common.by import By


class LoginModalLocators(object):

    CLOSE_BUTTON = (By.CSS_SELECTOR, '#section .header-modal span')
    CLOSE_BUTTON_DESC = 'Close login modal (X)'
