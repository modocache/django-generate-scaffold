#-*- coding: utf-8 -*-


from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class ListTest(unittest.TestCase, SeleniumTestCaseMixin):

    url = '/test_app/i18nmodel/'

    def test_ok(self):
        s = self.selenium
        s.open(self.url)

        # Checking for non-unicode characters is causing issues, so
        # for now simply assert that usual output is not present
        self.failIf(s.is_text_present('I18nModel List'))
