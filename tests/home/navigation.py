import unittest

from base.setup import BaseTest


class HomeNavigationTest(BaseTest):
    def test_navigate_to_home(self):
        pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HomeNavigationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)