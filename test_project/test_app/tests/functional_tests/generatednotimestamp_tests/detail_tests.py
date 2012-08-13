from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class DetailTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generatednotimestamp_model.json']
    url = '/test_app/generatednotimestampmodel/1/'

    def test_ok(self):
        s = self.selenium
        s.open(self.url)

        self.failUnless(s.is_text_present('GeneratedNoTimestampModel Detail'))
        self.failUnless(s.is_text_present('Generated No Timestamp Model Fixture'))

    def test_update(self):
        s = self.selenium
        s.open(self.url)
        s.click('link=Update')
        s.wait_for_page_to_load('30000')

        self.failUnless(s.is_text_present('GeneratedNoTimestampModel Update'))

    def test_no_timestamps(self):
        s = self.selenium
        s.open(self.url)

        self.failIf(s.is_text_present('created_at'))
        self.failIf(s.is_text_present('updated_at'))
