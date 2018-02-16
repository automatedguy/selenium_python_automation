import os
import sys
import logging
import unittest
from selenium import webdriver
import page

from base.constants import ALMUNDO_COM, CHROME, ARGENTINA, FIREFOX, VALID_BROWSERS, SETTING_UP, TEARING_DOWN

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class BaseTest(unittest.TestCase):
    BROWSER = CHROME
    COUNTRY = ARGENTINA

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    @classmethod
    def setUpClass(cls):
        """Run our `setUp` method on inherited classes, """
        if cls is not BaseTest and cls.setUp is not BaseTest.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                BaseTest.setUp(self)
                return orig_setUp(self, *args, **kwargs)

            cls.setUp = setUpOverride

    def setUp(self):
        pass

        self.logger.info(SETTING_UP + self.BROWSER)
        if self.BROWSER == CHROME:
            self.driver = webdriver.Chrome(PATH("../resources/chromedriver"))

        elif self.BROWSER == FIREFOX:
            self.driver = webdriver.Firefox()
        else:
            self.logger(VALID_BROWSERS + CHROME + ' - ' + FIREFOX)

        self.driver.maximize_window()
        self.driver.get(ALMUNDO_COM)

    def tearDown(self):
        pass

        self.logger.info(TEARING_DOWN + self.BROWSER)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
