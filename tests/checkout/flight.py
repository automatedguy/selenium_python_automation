import unittest

from base.setup import BaseTest
from base.setup import logger


class FlightTest(BaseTest):
    checkout_route = 'checkout/'
    product_route = '?product=flights'

    def setUp(self):
        pass

        logger.info("Wrapping up checkout URL...")
        self.checkout_url = self.base_url + self.checkout_route + self.cart_id + self.product_route

    def test_sheet_grid(self):
        pass
        logger.info('Opening checkout URL: [' + self.checkout_url + ']')
        self.driver.get(self.checkout_url)
        logger.info('Just for the wait...')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FlightTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
