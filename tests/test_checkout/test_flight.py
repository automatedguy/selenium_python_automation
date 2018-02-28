
from base.setup import *


class FlightTest(BaseTest):

    # Test parameters
    product_route = '?product=flights'
    origin = BaseTest.get_flight_origin()
    destination = 'MIA'
    departure_date = 50
    return_date = departure_date + 20
    adults = '1'
    children = '1'
    infants = '1'

    def setUp(self):
        self.api_host = self.get_api_host()
        self.channel = self.get_channel()
        self.country_site = self.get_country_site()
        self.country_language = self.get_country_language()

        self.cart_id = self.get_flight_cart_id(self.origin, self.destination,
                                               self.get_date(self.departure_date), self.get_date(self.return_date),
                                               self.country_site, self.country_language,
                                               self.adults, self.children, self.infants)

    def test_no_parameter(self):
        """ Load test_checkout without additional parameters"""
        checkout_parameter = ''

        checkout = self.open_checkout(self.cart_id, checkout_parameter, self.product_route)
        checkout.populate_checkout_info(self.channel, self.api_host, self.country_site, self.country_language)

        logger.info('Just for the wait...')

    def test_sc_enabled(self):
        """ Load test_checkout with &sc=1 """
        checkout_parameter = SC_ENABLED

        checkout = self.open_checkout(self.cart_id, checkout_parameter, self.product_route)
        checkout.populate_checkout_info(self.input_definitions)

        logger.info('Just for the wait...')

    def test_sw_cpd(self):
        """ Load test_checkout with &sw=cpd """
        checkout_parameter = SW_CPD

        checkout = self.open_checkout(self.cart_id, checkout_parameter, self.product_route)
        checkout.populate_checkout_info(self.input_definitions)

        logger.info('Just for the wait...')

    def test_sw_cpds(self):
        """ Load test_checkout with &sw=cpds """
        pass
        checkout_parameter = SW_CPDS

        checkout = self.open_checkout(self.cart_id, checkout_parameter, self.product_route)
        checkout.populate_checkout_info(self.input_definitions)

        logger.info('Just for the wait...')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FlightTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
