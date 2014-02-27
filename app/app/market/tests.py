from django.test import TestCase
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import selenium.webdriver.support.ui as ui
import haystack

class MarketSeleniumTests(LiveServerTestCase):
    fixtures = ['test_data.json']

    @classmethod
    def setUpClass(cls):
        haystack.connections.reload('default')
        cls.selenium = WebDriver()
        cls.wait = ui.WebDriverWait(cls.selenium,1000)
        super(MarketSeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        call_command('clear_index', interactive=False, verbosity=0)
        cls.selenium.quit()
        super(MarketSeleniumTests, cls).tearDownClass()


    def login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_id("id_login")
        username_input.send_keys('Changizkhaan')
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys('123456')
        password_input.submit()
        selenium = self.selenium
        self.wait.until(lambda selenium: selenium.find_element_by_id("q"))

    def test_login(self):
        self.login()


    def test_market_search(self):
        self.login()
        search = self.selenium.find_element_by_id("q")
        search.send_keys('test')
        self.selenium.find_element_by_id("searchbtn").click()
        selenium = self.selenium
        self.wait.until(lambda selenium: selenium.find_element_by_class_name('market-place-item item-wrap'))
        a=2


#class MarketTest(TestCase):
    #fixtures = ['test-data.json']

    #def test_details(self):
        #response = self.client.get('/market/item/#2')
        #self.assertEqual(response.status_code, 200)

    #def test_index(self):
        #response = self.client.get('/market/item/#43')
        #self.assertEqual(response.status_code, 200)