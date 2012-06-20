"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from generate_scaffold.generators.base import BaseGenerator



class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        b = BaseGenerator('bollocks')
        self.assertEqual(1 + 1, 2)
