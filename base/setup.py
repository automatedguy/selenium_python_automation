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

# Test parameters
BASE_URL = ST_ALMUNDO_COM
BROWSER = CHROME
COUNTRY = ARGENTINA
FORCE_HEADLESS = False


class BaseTest(unittest.TestCase):
    base_url = BASE_URL
    browser = BROWSER
    country = COUNTRY

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    @classmethod
    def setUpClass(cls):
        """Run our `setUp` method on inherited classes, """
        if cls is not BaseTest and cls.setUp is not BaseTest.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                BaseTest.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            cls.setUp = setUpOverride

    def set_chrome(self):
        if 'jenkins' in socket.gethostname() or FORCE_HEADLESS:
            self.logger.info('Setting headless mode')
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
            # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
            self.driver = webdriver.Chrome(PATH("../resources/chromedriver"), chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome(PATH("../resources/chromedriver"))

    def set_firefox(self):
        self.driver = webdriver.Firefox()

    def set_nothing(self):
        self.fail(VALID_BROWSERS + CHROME + ' - ' + FIREFOX)

    def setUp(self):
        self.logger.info(SETTING_UP + self.browser)

        set_browser = {
            CHROME: self.set_chrome(),
            FIREFOX: self.set_firefox()
        }

        set_browser.get(self.browser, self.set_nothing())
        self.driver.maximize_window()
        self.base_url = self.base_url + self.get_country_domain()

    def tearDown(self):
        self.logger.info(TEARING_DOWN + BROWSER)
        self.driver.quit()

    def open_checkout(self, cart_id, checkout_parameter, product_route,
                      channel, api_host, country_site, country_language):
        self.domain_url = self.base_url
        checkout_route = 'checkout/'
        checkout_url = self.domain_url + checkout_route + cart_id + product_route + checkout_parameter
        self.logger.info('Opening checkout URL: [' + checkout_url + ']')
        self.driver.get(checkout_url)

        from base.page import Checkout
        return Checkout(self.driver, cart_id, channel, api_host, country_site, country_language)

    def open_checkout_ab_router(self, ab_router_url, channel, api_host, country_site, country_language):
        ab_checkout_url = 'https://' + ab_router_url
        self.logger.info('Opening AB checkout URL: [' + ab_checkout_url + ']')
        self.driver.get(ab_checkout_url)
        cart_id = ab_checkout_url[(ab_checkout_url.index('checkout/') + len('checkout/')):ab_checkout_url.index('?')]

        from base.page import Checkout
        return Checkout(self.driver, cart_id, channel, api_host, country_site, country_language)

    def get_country_domain(self):
        country_domain = {
            ARGENTINA: '.ar/',
            COLOMBIA: '.co/',
            MEXICO: '.mx/',
            BRASIL: '.br/'
        }
        self.logger.info('Getting country domain: [' + country_domain.get(self.country) + ']')
        return country_domain.get(self.country, 'Invalid Country' + self.country)

    def get_country_site(self):
        country_site = {
            ARGENTINA: 'ARG',
            COLOMBIA: 'COL',
            MEXICO: 'MEX',
            BRASIL: 'BRA'
        }
        self.logger.info('Getting country site: [' + country_site.get(self.country) + ']')
        return country_site.get(self.country, 'Invalid Country' + self.country)

    def get_country_currency(self):
        country_currency = {
            ARGENTINA: 'ARS',
            COLOMBIA: 'COL',
            MEXICO: 'MXN',
            BRASIL: 'BRS'
        }
        self.logger.info('Getting country currency: [' + country_currency.get(self.country) + ']')
        return country_currency.get(self.country, 'Invalid Country' + self.country)

    def get_country_language(self):
        country_language = {
            ARGENTINA: 'es',
            COLOMBIA: 'es',
            MEXICO: 'es',
            BRASIL: 'pt'
        }
        self.logger.info('Getting country language: [' + country_language.get(self.country) + ']')
        return country_language.get(self.country, 'Invalid Country' + self.country)

    def get_channel(self):
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
        self.logger.info('Getting channel name: [' + channel.get(self.base_url) + ']')
        return channel.get(self.base_url, 'Invalid URL')

    def get_api_host(self):
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
        self.logger.info('Getting API host: [' + api_host.get(self.base_url) + ']')
        return api_host.get(self.base_url, 'Invalid URL' + self.base_url)

    @staticmethod
    def get_date(add_days):
        time_now = datetime.datetime.now()
        new_time = time_now + datetime.timedelta(add_days)
        return new_time.strftime("%Y-%m-%d")

    def get_flight_origin(self):
        flight_origin = {
            ARGENTINA: 'BUE',
            COLOMBIA: 'BOG',
            MEXICO: 'MEX',
            BRASIL: 'SAO'
        }
        self.logger.info('Getting flight origin for ' + COUNTRY + ' :[' + flight_origin.get(self.country) + ']')
        return flight_origin.get(self.country)

if __name__ == "__main__":
    unittest.main(failfast=True)
