import unittest

from base.setup import BaseTest, logger
from constants import SC_ENABLED, SW_CPD, SW_CPDS
from base.services import get_flight_cart_id


class FlightTest(BaseTest):
    # Test parameters
    product_route = '?product=flights'
    origin = 'BUE'
    destination = 'MIA'
    departure_date = 20
    return_date = departure_date + 20
    adults = '2'
    children = '1'
    infants = '0'

    def setUp(self):
        self.cart_id = get_flight_cart_id(self.origin, self.destination,
                                          self.get_date(self.departure_date), self.get_date(self.return_date),
                                          self.get_country_site(), self.get_country_language(),
                                          self.adults, self.children, self.infants)

    def test_no_parameter(self):
        """ Load checkout without additional parameters"""
        checkout_parameter = ''

        checkout = self.open_checkout(self.cart_id, checkout_parameter)
        checkout.populate_checkout_info()

        logger.info('Just for the wait...')

    def test_sc_enabled(self):
        """ Load checkout with &sc=1 """
        checkout_parameter = SC_ENABLED
        self.open_checkout(self.get_cart_id(), checkout_parameter)

        logger.info('Just for the wait...')

    def test_sw_cpd(self):
        """ Load checkout with &sw=cpd """
        checkout_parameter = SW_CPD
        self.open_checkout(self.get_cart_id(), checkout_parameter)

        logger.info('Just for the wait...')

    def test_sw_cpds(self):
        """ Load checkout with &sw=cpds """
        pass
        checkout_parameter = SW_CPDS
        self.open_checkout(self.get_cart_id(), checkout_parameter)

        logger.info('Just for the wait...')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FlightTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
