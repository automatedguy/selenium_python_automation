
from base.setup import BaseTest, unittest
from base.constants import *
from base.services import Cart


class FlightTest(BaseTest):

    # Test parameters
    product_route = '?product=flights'
    departure_date = 50
    return_date = departure_date + 20
    adults = '1'
    children = '1'
    infants = '1'

    def setUp(self):
        self.origin = self.get_flight_origin()
        self.destination = 'MIA'

        self.cart_id = Cart(
            self.get_api_host(),
            self.get_channel(),
            self.get_country_site(),
            self.get_country_language()
        ).get_flight_cart_id(
            self.origin, self.destination,
            self.get_date(self.departure_date), self.get_date(self.return_date),
            self.adults, self.children, self.infants
        )

    def test_no_parameter(self):
        """ Load test_checkout without additional parameters"""

        checkout_parameter = ''
        cross_selling = True

        checkout = self.open_checkout(
            self.cart_id,
            checkout_parameter,
            self.product_route,
            self.get_channel(),
            self.get_api_host(),
            self.get_country_site(),
            self.get_country_language()
        )

        checkout.populate_sections(cross_selling)

        pass
        self.logger.info('Just for the wait...')

    def test_sc_enabled(self):
        """ Load test_checkout with &sc=1 """
        checkout_parameter = SC_ENABLED

        cross_selling = False

        checkout = self.open_checkout(
            self.cart_id,
            checkout_parameter,
            self.product_route,
            self.get_channel(),
            self.get_api_host(),
            self.get_country_site(),
            self.get_country_language()
        )

        checkout.populate_sections(cross_selling)

        pass
        self.logger.info('Just for the wait...')

    def test_stc_enabled(self):
        """ Load test_checkout with &stc=1 """
        checkout_parameter = SCT_ENABLED

        cross_selling = True

        checkout = self.open_checkout(
            self.cart_id,
            checkout_parameter,
            self.product_route,
            self.get_channel(),
            self.get_api_host(),
            self.get_country_site(),
            self.get_country_language()
        )

        checkout.populate_sections(cross_selling)

        pass
        self.logger.info('Just for the wait...')

    def test_sw_cpd(self):
        """ Load test_checkout with &sw=cpd """
        checkout_parameter = SW_CPD

        cross_selling = False

        checkout = self.open_checkout(
            self.cart_id,
            checkout_parameter,
            self.product_route,
            self.get_channel(),
            self.get_api_host(),
            self.get_country_site(),
            self.get_country_language()
        )

        checkout.populate_sections(cross_selling)

        pass
        self.logger.info('Just for the wait...')

    def test_sw_cpds(self):
        """ Load test_checkout with &sw=cpds """
        checkout_parameter = SW_CPDS

        cross_selling = True

        checkout = self.open_checkout(
            self.cart_id,
            checkout_parameter,
            self.product_route,
            self.get_channel(),
            self.get_api_host(),
            self.get_country_site(),
            self.get_country_language()
        )

        checkout.populate_sections(cross_selling)

        pass
        self.logger.info('Just for the wait...')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FlightTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
