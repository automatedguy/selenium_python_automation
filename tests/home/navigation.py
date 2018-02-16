import unittest

from base.setup import BaseTest
from page import LoginModal


class HomeNavigationTest(BaseTest):
    def test_navigate_to_home(self):
        pass

        login_modal = LoginModal(self.driver)
        login_modal.click_close_login_modal()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(HomeNavigationTest)
    unittest.TextTestRunner(verbosity=2).run(suite)