from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys

class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):  #1
        for arg in sys.argv:  #2
            if 'liveserver' in arg:  #3
                cls.server_url = 'http://' + arg.split('=')[1]  #4
                return  #5
        super().setUpClass()  #6
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    def tearDown(self):
        self.browser.quit()
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    
    
    
    




