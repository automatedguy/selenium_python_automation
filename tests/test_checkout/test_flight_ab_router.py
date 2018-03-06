from base.setup import *


class FlightTest(BaseTest):
    # Test parameters
    product = 'flights'
    product_route = '?product=' + product
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

    def test_one(self):
        """ Ab router redirection test handle dynamically whatever comes from router """

        add_cross_selling = True

        checkout = self.open_checkout_ab_router(self.ab_router_url, self.channel, self.api_host, self.country_site, self.country_language)

        checkout.populate_checkout_sections(add_cross_selling)

        logger.info('Just for the wait...')

    def test_two(self):
        """ Ab router redirection test handle dynamically whatever comes from router """

        add_cross_selling = True

        checkout = self.open_checkout_ab_router(self.ab_router_url, self.channel, self.api_host, self.country_site, self.country_language)

        checkout.populate_checkout_sections(add_cross_selling)

        logger.info('Just for the wait...')

    def test_three(self):
        """ Ab router redirection test handle dynamically whatever comes from router """

        add_cross_selling = True

        checkout = self.open_checkout_ab_router(self.ab_router_url, self.channel, self.api_host, self.country_site,
                                                self.country_language)

        checkout.populate_checkout_sections(add_cross_selling)

        logger.info('Just for the wait...')

    def test_four(self):
        """ Ab router redirection test handle dynamically whatever comes from router """

        add_cross_selling = False

        checkout = self.open_checkout_ab_router(self.ab_router_url, self.channel, self.api_host, self.country_site,
                                                self.country_language)

        checkout.populate_checkout_sections(add_cross_selling)

        checkout.save_input_definitions(self.product)

        logger.info('Just for the wait...')
