import datetime
import os
import socket
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from base.services import *

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
FORCE_HEADLESS = False


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
            if 'jenkins' in socket.gethostname() or FORCE_HEADLESS:
                logger.info('Setting headless mode')
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--window-size=1920x1080")
                # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
                self.driver = webdriver.Chrome(PATH("../resources/chromedriver"), chrome_options=chrome_options)
            else:
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

    def open_checkout(self, cart_id, checkout_parameter, product_route,
                      channel, api_host, country_site, country_language):

        self.domain_url = self.base_url
        checkout_route = 'checkout/'
        checkout_url = self.domain_url + checkout_route + cart_id + product_route + checkout_parameter

        logger.info('Opening checkout URL: [' + checkout_url + ']')

        self.driver.get(checkout_url)

        from base.page import Checkout
        return Checkout(self.driver, cart_id, channel, api_host, country_site, country_language)

    def open_checkout_ab_router(self, ab_router_url, channel, api_host, country_site, country_language):
        ab_checkout_url = 'https://' + ab_router_url
        logger.info('Opening AB checkout URL: [' + ab_checkout_url + ']')

        self.driver.get(ab_checkout_url)

        cart_id = ab_checkout_url[(ab_checkout_url.index('checkout/')+len('checkout/')):ab_checkout_url.index('?')]

        from base.page import Checkout
        return Checkout(self.driver, cart_id, channel, api_host, country_site, country_language)

    @staticmethod
    def get_country_domain():
        country_domain = {
            ARGENTINA: '.ar/',
            COLOMBIA: '.co/',
            MEXICO: '.mx/',
            BRASIL: '.br/'
        }
        logger.info('Getting country domain: [' + country_domain.get(COUNTRY) + ']')
        return country_domain.get(COUNTRY, 'Invalid Country' + COUNTRY)

    @staticmethod
    def get_country_site():
        country_site = {
            ARGENTINA: 'ARG',
            COLOMBIA: 'COL',
            MEXICO: 'MEX',
            BRASIL: 'BRA'
        }
        logger.info('Getting country site: [' + country_site.get(COUNTRY) + ']')
        return country_site.get(COUNTRY, 'Invalid Country' + COUNTRY)

    @staticmethod
    def get_country_currency():
        country_currency = {
            ARGENTINA: 'ARS',
            COLOMBIA: 'COL',
            MEXICO: 'MXN',
            BRASIL: 'BRS'
        }
        logger.info('Getting country currency: [' + country_currency.get(COUNTRY) + ']')
        return country_currency.get(COUNTRY, 'Invalid Country' + COUNTRY)

    @staticmethod
    def get_country_language():
        country_language = {
            ARGENTINA: 'es',
            COLOMBIA: 'es',
            MEXICO: 'es',
            BRASIL: 'pt'
        }
        logger.info('Getting country language: [' + country_language.get(COUNTRY) + ']')
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
        logger.info('Getting channel name: [' + channel.get(BASE_URL) + ']')
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
        logger.info('Getting API host: [' + api_host.get(BASE_URL) + ']')
        return api_host.get(BASE_URL, 'Invalid URL' + BASE_URL)

    @staticmethod
    def get_date(add_days):
        time_now = datetime.datetime.now()
        new_time = time_now + datetime.timedelta(add_days)
        return new_time.strftime("%Y-%m-%d")

    @staticmethod
    def get_flight_origin():
        flight_origin = {
            ARGENTINA: 'BUE',
            COLOMBIA: 'BOG',
            MEXICO: 'MEX',
            BRASIL: 'SAO'
        }
        logger.info('Getting flight origin for ' + COUNTRY + ' :[' + flight_origin.get(COUNTRY) + ']')
        return flight_origin.get(COUNTRY)

    def get_flight_cart_id(self, origin, destination, departure_date, return_date, site, language, adults, children, infants):
        apikeys = Apikeys()
        channel_apikey = apikeys.get_apikey(BaseTest.get_channel())

        flights_clusters = FlightsClusters(BaseTest.get_api_host(), origin, destination, departure_date, return_date,
                                           site, language,
                                           adults, children, infants)

        product_id = flights_clusters.get_flight_id(channel_apikey)
        try:
            logger.info('Flight ID: [' + product_id + ']')
        except TypeError as no_availability:
            logger.error(ERR_NO_AVAILABILITY + str(no_availability))
            self.tearDown()
            self.fail()

        cart = Cart(BaseTest.get_api_host(), site, language)
        cart_id = cart.get_cart_id(channel_apikey, product_id)

        return cart_id

    @staticmethod
    def get_flight_ab_router_url(origin, destination, departure_date, return_date, site, language, adults, children, infants):
        apikeys = Apikeys()
        channel_apikey = apikeys.get_apikey(BaseTest.get_channel())

        flights_clusters = FlightsClusters(BaseTest.get_api_host(), origin, destination, departure_date, return_date,
                                           site, language,
                                           adults, children, infants)

        product_id = flights_clusters.get_flight_id(channel_apikey)
        logger.info('Flight ID: [' + product_id + ']')

        ab_router = AbRouterUrl(BASE_URL + BaseTest.get_country_domain(), site, language)
        ab_router_url = ab_router.get_ab_router_cart_id(channel_apikey, product_id)

        return ab_router_url


if __name__ == "__main__":
    unittest.main(failfast=True)
