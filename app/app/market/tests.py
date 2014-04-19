from django.test import TestCase
from django.conf import settings
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import selenium.webdriver.support.ui as ui
import time


class MarketSeleniumTests(LiveServerTestCase):
    fixtures = ['test_data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.wait = ui.WebDriverWait(cls.selenium,1000)
        super(MarketSeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MarketSeleniumTests, cls).tearDownClass()


    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_id("id_login")
        username_input.send_keys('manis')
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys('123456')
        password_input.submit()
        selenium = self.selenium
        self.wait.until(lambda selenium: selenium.find_element_by_id("q"))


    def test_market_search(self):
        self.login()
        time.sleep(2)
        search = self.selenium.find_element_by_id("q")
        search.send_keys('best')
        self.selenium.find_element_by_id("searchbtn").click()
        selenium = self.selenium
        self.wait.until(lambda selenium: selenium.find_element_by_class_name('market-place-item'))

