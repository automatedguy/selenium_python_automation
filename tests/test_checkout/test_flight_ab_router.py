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

        self.ab_router_url = self.get_flight_ab_router_url(self.origin, self.destination,
                                                           self.get_date(self.departure_date),
                                                           self.get_date(self.return_date),
                                                           self.country_site, self.country_language,
                                                           self.adults, self.children, self.infants)

    def test_no_parameter(self):
        """ Load test_checkout without additional parameters"""

        add_cross_selling = True

        checkout = self.open_checkout_ab_router(self.ab_router_url, self.channel, self.api_host, self.country_site, self.country_language)

        checkout.populate_checkout_info(add_cross_selling)

        logger.info('Just for the wait...')
