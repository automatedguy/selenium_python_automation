import unittest

from base.setup import BaseTest
from base.setup import logger


class HotelTest(BaseTest):

    product_route = '?product=hotel'

    def test_no_parameter(self):
        pass
        checkout_parameter = ''
        self.open_checkout(checkout_parameter)

        logger.info('Just for the wait...')

    def test_sc_enabled(self):
        pass
        checkout_parameter = '&sc=1'
        self.open_checkout(checkout_parameter)

        logger.info('Just for the wait...')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HotelTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
