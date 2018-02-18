import os
import logging
import unittest
from selenium import webdriver

from base.constants import ALMUNDO_COM, CHROME, ARGENTINA, FIREFOX, VALID_BROWSERS, SETTING_UP, TEARING_DOWN

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Test parameters
BASE_URL = ALMUNDO_COM
BROWSER = CHROME
COUNTRY = ARGENTINA
CART_ID = '5a89eaec24aa9a000b76f9f0'
CHECKOUT_PARAMETER = '&sc=1'


def get_country_domain():
    country_domain = {
        'Argentina': '.ar/',
        'Colombia': '.co/',
        'Mexico': '.mx/',
        'Brasil': '.br/'
    }
    print
    return country_domain.get(COUNTRY, "Invalid Country" + COUNTRY)


class BaseTest(unittest.TestCase):

    base_url = BASE_URL
    browser = BROWSER
    country = COUNTRY
    cart_id = CART_ID

    @classmethod
    def setUpClass(cls):
        """Run our `setUp` method on inherited classes, """
        if cls is not BaseTest and cls.setUp is not BaseTest.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                BaseTest.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            cls.setUp = setUpOverride

    def setUp(self):
        pass

        logger.info(SETTING_UP + self.browser)

        if self.browser == CHROME:
            self.driver = webdriver.Chrome(PATH("../resources/chromedriver"))
        elif self.browser == FIREFOX:
            self.driver = webdriver.Firefox()
        else:
            logger(VALID_BROWSERS + CHROME + ' - ' + FIREFOX)
        self.driver.maximize_window()

        if CART_ID is not '':
            self.base_url = self.base_url + get_country_domain()
        else:
            self.driver.get(BASE_URL)

    def tearDown(self):
        pass

        logger.info(TEARING_DOWN + BROWSER)
        self.driver.quit()


class CheckoutTest(BaseTest):

    def setUp(self):
        pass

        checkout_route = 'checkout/'

        logger.info("Wrapping up checkout URL.")
        self.checkout_url = self.base_url + checkout_route + self.cart_id + self.product_route

    def open_checkout(self, checkout_parameter):
        logger.info('Opening checkout URL: [' + self.checkout_url + checkout_parameter + ']')
        self.driver.get(self.checkout_url + checkout_parameter)


if __name__ == "__main__":
    unittest.main()
