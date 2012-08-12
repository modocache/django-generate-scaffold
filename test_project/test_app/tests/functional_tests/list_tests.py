from django.utils import unittest
from noseselenium.cases import SeleniumTestCaseMixin


class ListTest(unittest.TestCase, SeleniumTestCaseMixin):

    def test_ok(self):
        s = self.selenium
        s.open("/test_app/generatedmodel/")
        self.failUnless(
            s.is_text_present('A page representing a list of objects.'))
