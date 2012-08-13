from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class ListTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generatednotimestamp_model.json']
    url = '/test_app/generatednotimestampmodel/'

    def test_ok(self):
        s = self.selenium
        s.open(self.url)
        self.failUnless(s.is_text_present('GeneratedNoTimestampModel List'))

    def test_click_on_item(self):
        s = self.selenium
        s.open(self.url)
        s.click('link=001')
        s.wait_for_page_to_load('30000')

        self.failUnless(s.is_text_present('GeneratedNoTimestampModel Detail'))
        self.failUnless(s.is_text_present('Generated No Timestamp Model Fixture'))
