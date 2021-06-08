#!/usr/bin/env python3

import unittest

from Progress import ProgressPie

class TestProgressPie(unittest.TestCase):
    def test_colors(self):
        testcases = [
            {"circle": [50, 50, 50], "percentage": 0, "point": [55, 55], "expected": "white" },
            {"circle": [50, 50, 50], "percentage": 12, "point": [55, 55], "expected": "white"},
            {"circle": [50, 50, 50], "percentage": 13, "point": [55, 55], "expected": "black"},
            {"circle": [50, 50, 50], "percentage": 99, "point": [99, 99], "expected": "white"},
            {"circle": [50, 50, 50], "percentage": 87, "point": [20, 40], "expected": "black"},
        ]

        for testc in testcases:
            pp = ProgressPie(testc["circle"][0], testc["circle"][1], testc["circle"][2])
            result = pp.QueryPoint(testc["point"][0], testc["point"][1], testc["percentage"])
            self.assertEqual(result, testc["expected"])

"""
 ~/Pyc/ProgressPie  master !1 ?2  python3 -m unittest test_Progress.py -v              1 ✘  Py395_default 
test_colors (test_Progress.TestProgressPie) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
"""
