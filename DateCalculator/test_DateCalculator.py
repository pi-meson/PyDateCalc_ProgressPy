#!/usr/bin/env python3

import unittest
import datetime

from DateCalculator import DateCalculator
from DateCalculator import DateCalculatorException


class TestDateCalculator(unittest.TestCase):
    def test_invalid_date1(self):
        with self.assertRaises(DateCalculatorException):
            dc = DateCalculator("02-061983", "22-06-1983")
            dc.DateDiffCalc()

    def test_invalid_date2(self):
        with self.assertRaises(DateCalculatorException):
            dc = DateCalculator("02-06-1983", "2206-1983")
            dc.DateDiffCalc()

    def test_valid_dates(self):
        dc = DateCalculator("02-06-1983", "22-06-1983")
        self.assertEqual(dc.DateDiffCalc(), 19)

    def test_valid_dates_compare_with_datetime(self):
        d1 = datetime.date(1983, 6, 2)
        d2 = datetime.date(1983, 6, 22)
        dc = DateCalculator("02-06-1983", "22-06-1983")
        self.assertEqual(dc.DateDiffCalc(), (d2-d1).days - 1)

    def test_valid_dates_out_of_order(self):
        dc = DateCalculator("03-01-1989", "03-08-1983")
        self.assertEqual(dc.DateDiffCalc(), 1979)


"""
Run example:
    python3 -m unittest test_DateCalculator.py -v
"""
