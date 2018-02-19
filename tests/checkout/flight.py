import unittest

from base.setup import CheckoutTest, get_country_site, get_country_language, get_date
from base.setup import logger
from constants import SC_ENABLED, SW_CPD, SW_CPDS
from services import get_flight_cart_id


class FlightTest(CheckoutTest):
    # Test parameters
    product_route = '?product=flights'
    origin = 'BUE'
    destination = 'MIA'
    departure_date = 20
    return_date = departure_date + 20
    adults = '2'
    children = '1'
    infants = '0'

    def test_no_parameter(self):
        pass
        checkout_parameter = ''
        self.open_checkout(get_flight_cart_id(self.origin, self.destination,
                                              get_date(self.departure_date), get_date(self.return_date),
                                              get_country_site(), get_country_language(),
                                              self.adults, self.children, self.infants),
                           checkout_parameter)

        logger.info('Just for the wait...')

    def test_sc_enabled(self):
        pass
        checkout_parameter = SC_ENABLED
        self.open_checkout(get_flight_cart_id(self.origin, self.destination,
                                              get_date(self.departure_date), get_date(self.return_date),
                                              get_country_site(), get_country_language(),
                                              self.adults, self.children, self.infants),
                           checkout_parameter)

        logger.info('Just for the wait...')

    def test_sw_cpd(self):
        pass
        checkout_parameter = SW_CPD
        self.open_checkout(get_flight_cart_id(self.origin, self.destination,
                                              get_date(self.departure_date), get_date(self.return_date),
                                              get_country_site(), get_country_language(),
                                              self.adults, self.children, self.infants),
                           checkout_parameter)

        logger.info('Just for the wait...')

    def test_sw_cpds(self):
        pass
        checkout_parameter = SW_CPDS
        self.open_checkout(get_flight_cart_id(self.origin, self.destination,
                                              get_date(self.departure_date), get_date(self.return_date),
                                              get_country_site(), get_country_language(),
                                              self.adults, self.children, self.infants),
                           checkout_parameter)

        logger.info('Just for the wait...')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FlightTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
