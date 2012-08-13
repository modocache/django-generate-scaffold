from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class ArchiveWeekTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generated_model.json']
    url = '/test_app/generatedmodel/archive/2012/8/week/32/'

    def setUp(self):
        self.selenium.open(self.url)

    def test_ok(self):
        s = self.selenium
        self.failUnless(s.is_text_present('GeneratedModel Week Archive'))
        self.failUnless(s.is_text_present('Generated Model Fixture'))
