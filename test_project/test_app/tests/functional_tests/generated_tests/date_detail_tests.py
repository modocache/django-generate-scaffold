from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class DateDetailTest(unittest.TestCase, SeleniumTestCaseMixin):

    selenium_fixtures = ['test_generated_model.json']
    url = '/test_app/generatedmodel/2012/8/11/1/'

    def setUp(self):
        self.selenium.open(self.url)

    def test_ok(self):
        s = self.selenium
        self.failUnless(s.is_text_present('GeneratedModel Detail'))
        self.failUnless(s.is_text_present('Generated Model Fixture'))

    def test_link_date_detail(self):
        s = self.selenium
        s.click('link=Date Detail')
        s.wait_for_page_to_load('30000')
        self.failUnless(s.is_text_present('GeneratedModel Detail'))
        self.failUnless(s.is_text_present('Generated Model Fixture'))

    def test_link_day_archive(self):
        s = self.selenium
        s.click('link=Day Archive')
        s.wait_for_page_to_load('30000')
        self.failUnless(s.is_text_present('GeneratedModel Day Archive'))

    def test_link_month_archive(self):
        s = self.selenium
        s.click('link=Month Archive')
        s.wait_for_page_to_load('30000')
        self.failUnless(s.is_text_present('GeneratedModel Month Archive'))

    def test_link_year_archive(self):
        s = self.selenium
        s.click('link=Year Archive')
        s.wait_for_page_to_load('30000')
        self.failUnless(s.is_text_present('GeneratedModel Year Archive'))

    def test_link_archive_index(self):
        s = self.selenium
        s.click('link=Archive Index')
        s.wait_for_page_to_load('30000')
        self.failUnless(s.is_text_present('GeneratedModel Archive Index'))
