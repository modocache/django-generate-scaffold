from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class ArchiveIndexTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generated_model.json']
    url = '/test_app/generatedmodel/archive/'

    def setUp(self):
        self.selenium.open(self.url)

    def test_ok(self):
        s = self.selenium
        self.failUnless(s.is_text_present('GeneratedModel Archive Index'))
        self.failUnless(s.is_text_present('Generated Model Fixture'))

    def test_year_list(self):
        s = self.selenium
        s.click('link=2012')
        s.wait_for_page_to_load('30000')
        self.failUnless(s.is_text_present('GeneratedModel Year Archive'))

    def test_link_archive_index(self):
        s = self.selenium
        s.click('link=Archive Index')
        s.wait_for_page_to_load('30000')
        self.failUnless(s.is_text_present('GeneratedModel Archive Index'))
