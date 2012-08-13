from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class DetailTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generated_model.json']
    url = '/test_app/generatedmodel/1/'

    def test_ok(self):
        s = self.selenium
        s.open(self.url)

        self.failUnless(s.is_text_present('GeneratedModel Detail'))
        self.failUnless(s.is_text_present('Generated Model Fixture'))

    def test_update(self):
        s = self.selenium
        s.open(self.url)
        s.click('link=Update')
        s.wait_for_page_to_load('30000')

        self.failUnless(s.is_text_present('GeneratedModel Update'))

    def test_timetstamps(self):
        s = self.selenium
        s.open(self.url)

        self.failUnless(s.is_text_present('created_at'))
        self.failUnless(s.is_text_present('updated_at'))
