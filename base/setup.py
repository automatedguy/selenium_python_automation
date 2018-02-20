import os
import logging
import unittest
import datetime
from selenium import webdriver

from base.constants import *

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Test parameters
BASE_URL = ST_ALMUNDO_COM
BROWSER = CHROME
COUNTRY = ARGENTINA
CHECKOUT_PARAMETER = '&sc=1'


def get_country_domain():
    country_domain = {
        'Argentina': '.ar/',
        'Colombia': '.co/',
        'Mexico': '.mx/',
        'Brasil': '.br/'
    }
    return country_domain.get(COUNTRY, "Invalid Country" + COUNTRY)


def get_country_site():
    country_site = {
        'Argentina': 'ARG',
        'Colombia': 'COL',
        'Mexico': 'MEX',
        'Brasil': 'BRA'
    }
    return country_site.get(COUNTRY, "Invalid Country" + COUNTRY)


def get_country_currency():
    country_site = {
        'Argentina': 'ARS',
        'Colombia': 'COL',
        'Mexico': 'MXN',
        'Brasil': 'BRS'
    }
    return country_site.get(COUNTRY, "Invalid Country" + COUNTRY)


def get_country_language():
    country_language = {
        'Argentina': 'es',
        'Colombia': 'es',
        'Mexico': 'es',
        'Brasil': 'pt'
    }
    return country_language.get(COUNTRY, "Invalid Country" + COUNTRY)


def get_date(add_days):
    time_now = datetime.datetime.now()
    new_time = time_now + datetime.timedelta(add_days)
    return new_time.strftime("%Y-%m-%d")


class BaseTest(unittest.TestCase):
    base_url = BASE_URL
    browser = BROWSER
    country = COUNTRY

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
        self.base_url = self.base_url + get_country_domain()

    def tearDown(self):
        pass

        logger.info(TEARING_DOWN + BROWSER)
        self.driver.quit()


class CheckoutTest(BaseTest):
    def setUp(self):
        pass
        checkout_route = 'checkout/'

        logger.info("Wrapping up checkout URL.")
        self.domain_url = self.base_url + checkout_route

    def open_checkout(self, cart_id, checkout_parameter):
        checkout_url = self.domain_url \
                        + cart_id + self.product_route \
                        + checkout_parameter

        logger.info('Opening checkout URL: [' + checkout_url + ']')

        self.driver.get(checkout_url)


if __name__ == "__main__":
    unittest.main()
