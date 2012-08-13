from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class UpdateTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generatednotimestamp_model.json']
    url = '/test_app/generatednotimestampmodel/1/update/'

    def test_ok(self):
        s = self.selenium
        s.open(self.url)
        self.failUnless(s.is_text_present('GeneratedNoTimestampModel Update'))

    def test_update(self):
        s = self.selenium
        s.open(self.url)
        s.type('id_title', 'No Timestamp Model Fixture Update!')
        s.click('css=button[type="submit"]')
        s.wait_for_page_to_load('30000')

        self.failUnless(s.is_text_present('GeneratedNoTimestampModel Detail'))
        self.failUnless(s.is_text_present('No Timestamp Model Fixture Update!'))
