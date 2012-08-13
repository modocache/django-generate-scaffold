from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class CreateTest(unittest.TestCase, SeleniumTestCaseMixin):

    url = '/test_app/generatednotimestampmodel/create/'

    def test_ok(self):
        s = self.selenium
        s.open(self.url)
        self.failUnless(s.is_text_present('GeneratedNoTimestampModel Create'))

    def test_create(self):
        s = self.selenium
        s.open(self.url)
        s.type('id_title', 'My Generated No Timestamp Model')
        s.type('id_description', 'This is a new instance of my model.')
        s.click('css=button[type="submit"]')
        s.wait_for_page_to_load('30000')

        self.failUnless(s.is_text_present('GeneratedNoTimestampModel Detail'))
        self.failUnless(s.is_text_present('My Generated No Timestamp Model'))
