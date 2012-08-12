from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class DeleteTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generated_model.json']
    url = '/test_app/generatedmodel/1/'

    def test_delete(self):
        s = self.selenium

        # Ensure fixture model is displayed on list view
        s.open('/test_app/generatedmodel/')
        self.failUnless(s.is_text_present('GeneratedModel List'))
        self.failUnless(s.is_text_present('Generated Model Fixture'))

        # Open detail view
        s.open('/test_app/generatedmodel/1/')
        self.failUnless(s.is_text_present('GeneratedModel Detail'))
        self.failUnless(s.is_text_present('Generated Model Fixture'))
        # Click Delete button
        s.click('css=button[type="submit"]')
        s.wait_for_page_to_load('30000')

        # Ensure fixture model is no longer displayed on list view
        self.failUnless(s.is_text_present('GeneratedModel List'))
        self.failIf(s.is_text_present('Generated Model Fixture'))
