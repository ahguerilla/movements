from django.test import TestCase
from django.conf import settings
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import selenium.webdriver.support.ui as ui
import pysolr
import haystack
from django.core.management import call_command


class SolrTestCase(LiveServerTestCase):
    fixtures = ['test_data.json']
    longMessage = True
    solrCoreAdminPath = 'admin/cores'

    def setUp(self):
        haystack.connections.reload('testing')
        call_command('rebuild_index', using=('testing',), interactive=False, verbosity=0)
        self.old_solr_url = settings.HAYSTACK_CONNECTIONS['default']['URL']

        from haystack.management.commands.build_solr_schema \
            import Command as BuildSolrSchemaCommand
        cmd = BuildSolrSchemaCommand()

        import os
        instance_dir = os.path.join(settings.PROJECT_PATH, 'fixtures', 'solr_test')
        conf_dir = os.path.join(instance_dir, 'conf')
        cmd.handle(using="testing", filename=os.path.join(conf_dir, "schema.xml"))

        from pysolr import SolrError
        try:
            admin = pysolr.SolrCoreAdmin(url='%s/%s' %
                (self.old_solr_url , self.solrCoreAdminPath))
            admin.create(name='test_core', instance_dir=instance_dir)
        except SolrError as e:
            raise SolrError("Unable to create a new disposable core. Have "
                "you configured Solr to enable multiple cores as described "
                "at http://docs.lucidworks.com/display/solr/Core+Admin+and+Configuring+solr.xml? "
                "%s" % e)

        self.solr = pysolr.Solr(settings.HAYSTACK_CONNECTIONS['testing']['URL'])
        self.solr.delete(q='*:*')

        a=haystack.connections['testing']
        b=a.get_backend()
        c = b.build_models_list()
        p=2

        # poke into haystack backends to change URL of any backend that's
        # already registered.

        #from haystack.backends.solr_backend import SearchBackend as SolrSearchBackend
        #for index in site.get_indexes().values():
            #if isinstance(index.backend, SolrSearchBackend) and not getattr(index.backend, '_old_conn', None):
                #index.backend._old_conn = index.backend.conn
                #index.backend.conn = self.solr

    def tearDown(self):
        pass
        #settings.HAYSTACK_SOLR_URL = self.old_solr_url
        #from haystack.sites import site
        #from haystack.backends.solr_backend import SearchBackend as SolrSearchBackend
        #for index in site.get_indexes().values():
            #if isinstance(index.backend, SolrSearchBackend):
                #index.backend.conn = index.backend._old_conn


class MarketSeleniumTests(SolrTestCase):
    @classmethod
    def setUpClass(cls):
        super(MarketSeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()
        cls.wait = ui.WebDriverWait(cls.selenium,1000)

    @classmethod
    def tearDownClass(cls):
        #call_command('clear_index', using=('testing',), interactive=False, verbosity=0)
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

    #def test_login(self):
        #self.login()


    def test_market_search(self):
        self.login()
        search = self.selenium.find_element_by_id("q")
        search.send_keys('best')
        self.selenium.find_element_by_id("searchbtn").click()
        selenium = self.selenium
        self.wait.until(lambda selenium: selenium.find_element_by_class_name('market-place-item item-wrap'))
        a=2


#class MarketTest(TestCase):
    #fixtures = ['test_data.json']

    #@classmethod
    #def setUpClass(cls):
        #haystack.connections.reload('testing')
        #haystack.management.commands.rebuild_index()
        #super(TestCase, cls).setUpClass()

    #def test_details(self):
        #response = self.client.get('/market/item/#2')
        #self.assertEqual(response.status_code, 200)

    #def test_index(self):
        #response = self.client.get('/market/item/#43')
        #self.assertEqual(response.status_code, 200)

    #@classmethod
    #def tearDownClass(cls):
        #pass


