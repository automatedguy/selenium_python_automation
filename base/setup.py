import os
import unittest
import datetime
from selenium import webdriver
from services import *

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
        self.base_url = self.base_url + self.get_country_domain()

    def tearDown(self):
        pass

        logger.info(TEARING_DOWN + BROWSER)
        self.driver.quit()

    def open_checkout(self, cart_id, checkout_parameter, product_route):
        self.domain_url = self.base_url
        checkout_route = 'checkout/'
        checkout_url = self.domain_url + checkout_route + cart_id + product_route + checkout_parameter

        logger.info('Opening checkout URL: [' + checkout_url + ']')

        self.driver.get(checkout_url)

        from page import Checkout
        return Checkout(self.driver, cart_id)

    @staticmethod
    def get_country_domain():
        country_domain = {
            ARGENTINA: '.ar/',
            COLOMBIA: '.co/',
            MEXICO: '.mx/',
            BRASIL: '.br/'
        }
        return country_domain.get(COUNTRY, 'Invalid Country' + COUNTRY)

    @staticmethod
    def get_country_site():
        country_site = {
            ARGENTINA: 'ARG',
            COLOMBIA: 'COL',
            MEXICO: 'MEX',
            BRASIL: 'BRA'
        }
        return country_site.get(COUNTRY, 'Invalid Country' + COUNTRY)

    @staticmethod
    def get_country_currency():
        country_site = {
            ARGENTINA: 'ARS',
            COLOMBIA: 'COL',
            MEXICO: 'MXN',
            BRASIL: 'BRS'
        }
        return country_site.get(COUNTRY, 'Invalid Country' + COUNTRY)

    @staticmethod
    def get_country_language():
        country_language = {
            ARGENTINA: 'es',
            COLOMBIA: 'es',
            MEXICO: 'es',
            BRASIL: 'pt'
        }
        return country_language.get(COUNTRY, 'Invalid Country' + COUNTRY)

    @staticmethod
    def get_channel():
        channel = {
            ALMUNDO_COM: 'almundo-web',
            ST_ALMUNDO_COM: 'almundo-web',
            DV_ALMUNDO_COM: 'almundo-web',

            CCR_ALMUNDO_COM: 'ccr',
            CCR_ST_ALMUNDO_COM: 'ccr',
            CCR_DV_ALMUNDO_COM: 'ccr',

            RET_ALMUNDO_COM: 'retail',
            RET_ST_ALMUNDO_COM: 'retail',
            RET_DV_ALMUNDO_COM: 'retail'
        }
        return channel.get(BASE_URL, 'Invalid URL')

    @staticmethod
    def get_api_host():
        api_host = {
            ALMUNDO_COM: API_ALMUNDO_COM,
            ST_ALMUNDO_COM: APIST_ALMUNDO_COM,
            DV_ALMUNDO_COM: APIDV_ALMUNDO_COM,

            CCR_ALMUNDO_COM: API_ALMUNDO_COM,
            CCR_ST_ALMUNDO_COM: APIST_ALMUNDO_COM,
            CCR_DV_ALMUNDO_COM: APIDV_ALMUNDO_COM,

            RET_ALMUNDO_COM: API_ALMUNDO_COM,
            RET_ST_ALMUNDO_COM: APIST_ALMUNDO_COM,
            RET_DV_ALMUNDO_COM: APIDV_ALMUNDO_COM,

        }
        return api_host.get(BASE_URL, 'Invalid URL' + BASE_URL)

    @staticmethod
    def get_date(add_days):
        time_now = datetime.datetime.now()
        new_time = time_now + datetime.timedelta(add_days)
        return new_time.strftime("%Y-%m-%d")

    @staticmethod
    def get_flight_cart_id(origin, destination, departure_date, return_date, site, language, adults, children, infants):
        apikeys = Apikeys()
        channel_apikey = apikeys.get_apikey()
        logger.info('X-apikey: [' + channel_apikey + ']')

        flights_clusters = FlightsClusters(origin, destination, departure_date, return_date,
                                           site, language,
                                           adults, children, infants)

        product_id = flights_clusters.get_flight_id(channel_apikey)
        logger.info('Flight ID: [' + product_id + ']')

        cart = Cart(site, language)
        cart_id = cart.get_cart_id(channel_apikey, product_id)

        return cart_id

    @staticmethod
    def get_input_definitions(cart_id):
        apikeys = Apikeys()
        channel_apikey = apikeys.get_apikey()
        input_definitions = InputDefinitions(BaseTest.get_api_host(), cart_id,
                                             BaseTest.get_country_site(),
                                             BaseTest.get_country_language()) \
            .get_input_definitions(channel_apikey)

        return input_definitions


if __name__ == "__main__":
    unittest.main()
