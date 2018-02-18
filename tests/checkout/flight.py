import unittest

from base.setup import BaseTest


class FlightTest(BaseTest):
    checkout_route = 'checkout/'
    product_route = '?product=flights'

    def setUp(self):
        pass

        self.logger.info("Wrapping up checkout URL...")
        self.checkout_url = self.BASE_URL \
                            + self.checkout_route \
                            + self.CART_ID \
                            + self.product_route

    def test_sheet_grid(self):
        pass
        self.logger.info('Opening checkout URL: [' + self.checkout_url + ']')
        self.driver.get(self.checkout_url)
        self.logger.info('Just for the wait...')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FlightTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
