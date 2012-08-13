from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class UpdateTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generated_model.json']
    url = '/test_app/generatedmodel/1/update/'

    def test_ok(self):
        s = self.selenium
        s.open(self.url)
        self.failUnless(s.is_text_present('GeneratedModel Update'))

    def test_update(self):
        s = self.selenium
        s.open(self.url)
        s.type('id_title', 'Generated Model Fixture Update!')
        s.click('css=button[type="submit"]')
        s.wait_for_page_to_load('30000')

        self.failUnless(s.is_text_present('GeneratedModel Detail'))
        self.failUnless(s.is_text_present('Generated Model Fixture Update!'))
