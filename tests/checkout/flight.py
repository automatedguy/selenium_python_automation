import unittest

from base.setup import CheckoutTest, get_country_site, get_country_language, get_date
from base.setup import logger
from constants import SC_ENABLED, SW_CPD, SW_CPDS


class FlightTest(CheckoutTest):

    # Test parameters
    product_route = '?product=flights'
    origin = 'BUE'
    destination = 'MIA'
    days_to_departure = 20
    days_to_return = days_to_departure + 20
    adults = '2'
    children = '1'
    infants = '0'

    def get_cart_id(self):
        get_country_site()
        get_country_language()
        get_date(self.days_to_departure)
        get_date(self.days_to_return)

        return '5a8a13c024aa9a000bfee1e6'

    def test_no_parameter(self):
        pass
        checkout_parameter = ''
        self.open_checkout(self.get_cart_id(), checkout_parameter)

        logger.info('Just for the wait...')

    def test_sc_enabled(self):
        pass
        checkout_parameter = SC_ENABLED
        self.open_checkout(self.get_cart_id(), checkout_parameter)

        logger.info('Just for the wait...')

    def test_sw_cpd(self):
        pass
        checkout_parameter = SW_CPD
        self.open_checkout(self.get_cart_id(), checkout_parameter)

        logger.info('Just for the wait...')

    def test_sw_cpds(self):
        pass
        checkout_parameter = SW_CPDS
        self.open_checkout(self.get_cart_id(), checkout_parameter)

        logger.info('Just for the wait...')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FlightTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
