import unittest

from page import LoginModal
from setup import BaseTest


class HomeNavigationTest(BaseTest):
    def setUp(self):
        login_modal = LoginModal(self.driver)
        login_modal.click_close_login_modal()

    def test_navigate_to_home(self):
        pass

        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HomeNavigationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
