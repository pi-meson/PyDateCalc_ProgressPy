#!/usr/bin/env python3

"""
DateCalculator is a command-line application to calculate the number of elapsed
days between two given days.

DateCalculator.py

Principal author: Abhishek Tiwary
                  ab.tiwary@gmail.com
"""

import re
import sys
import argparse

from typing import Tuple
from dataclasses import dataclass
from functools import reduce

@dataclass
class DateClass:
    day: int
    month: int
    year: int

class DateCalculatorException(Exception): pass

class DateCalculator:
    """
    The DateCalculator class contains logic to compute the number of elapsed days
    between two given dates. Instantiate this class and call the DateDiffCalc method.
    """
    def __init__(self, date1: str, date2: str):
        self.checkIfDatesAreValid(date1, date2)
        self.daysMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.date1 = date1
        self.date2 = date2
        self.DateObj1 = self.createDateObject(self.date1)
        self.DateObj2 = self.createDateObject(self.date2)

    def checkIfDatesAreValid(self, date1: str, date2: str):
        match1 = re.match("[0-9]{2}\-[0-9]{2}\-[0-9]{4}", date1)
        if match1 is None:
            raise DateCalculatorException("date1 is in an unknown format")

        match2 = re.match("[0-9]{2}\-[0-9]{2}\-[0-9]{4}", date2)
        if match2 is None:
            raise DateCalculatorException("date2 is in an unknown format")

    def createDateObject(self, dateStr) -> DateClass:
        dateSplit = dateStr.split('-')
        return DateClass(int(dateSplit[0]), int(dateSplit[1]), int(dateSplit[2]))

    def IsLeap(self, year: int) -> bool:
        """
        Given a year, represented as an int, compute whether it is a leap year.
        According to the most common algorithm, an year is a leap year (and thus
        spans 366 days) if it is divisible by 4 or 400, but not 100.

        :param year: the year, as in int
        :return: bool
        """
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        elif year % 4 == 0:
            return True
        return False

    def GetSortedDates(self, d1: DateClass, d2: DateClass) -> Tuple[DateClass, DateClass]:
        """
        Given two DateClass objects, return them in a tuple where they are in sorted order
        (ascending)

        :param d1: DateClass
        :param d2: DateClass
        :return: A tuple of two DateClass objects in sorted order
        """
        if d1.year == d2.year:
            if d1.month == d2.month:
                if d1.day == d2.day:
                    raise DateCalculatorException("dates are equal")
                return (d2, d1) if d1.day > d2.day else (d1, d2)
            return (d2, d1) if d1.month > d2.month else (d1, d2)
        return (d2, d1) if d1.year > d2.year else (d1, d2)

    def GetDayOfYear(self, dobj: DateClass) -> int:
        """
        Given a DateClass object, compute what day of the year it is - i.e. x out of 365
        (or 366 in case of a leap year)

        :param dobj: DateClass
        :return: int, representing the day number
        """
        dayOfYear = 0

        if dobj.month > 1:
            dayOfYear = reduce(lambda x, y: x + y, self.daysMonth[:(dobj.month - 1)])

        dayOfYear += dobj.day
        if self.IsLeap(dobj.year) and dobj.month > 2:
            dayOfYear += 1
        return dayOfYear

    def DateDiffCalc(self) -> int:
        """
        Call the DateDiffCalc method to get the number of days elapsed.

        The algorithm is roughly:
        - Sort the two dates from earlier to later
        - Calculate if the start date (earlier) is for a leap year
        - Calculate what day number in the year both are
        - If the later date is in a different year, start adding the number of days to the
          running total until the target year is reached, then add the number of days denoting
          the day number of the target date and subtract one to exclude the last date.
        - Else, perform a simple subtraction, and subtract 1 to exclude the last date.

        :return: int, the number of days elapsed between two given dates - does not include
            the first and the last date
        """
        try:
            startDate, endDate = self.GetSortedDates(self.DateObj1, self.DateObj2)

            startDateIsLeap = self.IsLeap(startDate.year)

            dayOfYearStart = self.GetDayOfYear(startDate)
            dayOfYearEnd = self.GetDayOfYear(endDate)

            total = 0
            if startDate.year < endDate.year:
                yearToEndStart = (366 - dayOfYearStart) if startDateIsLeap else (365 - dayOfYearStart)
                total += yearToEndStart

                startYear = startDate.year + 1
                while startYear < endDate.year:
                    total = (total + 366) if self.IsLeap(startYear) else (total + 365)
                    startYear += 1
                total += dayOfYearEnd - 1
            else:
                total = dayOfYearEnd - dayOfYearStart - 1

            return total

        except DateCalculatorException as e:
            print(sys.stderr, e)
            return 0

def main(args):
    dc = DateCalculator(args.date1, args.date2)
    print(f"{dc.DateDiffCalc()} days elapsed")



if __name__ == "__main__":
    options = argparse.ArgumentParser(description="Calculate the diff between two dates")
    options.add_argument("--date1", dest="date1", help="The first date, in format dd-mm-yyyy", required=True)
    options.add_argument("--date2", dest="date2", help="The second date, in format dd-mm-yyyy", required=True)
    args = options.parse_args()

    try:
        main(args)
    except DateCalculatorException as e:
        print(f"An exception occurred: {str(e)}", file=sys.stderr)


"""" 
Example invocations:
 ~/PycharmProjects/DateCalculator  ./DateCalculator.py --date1 02-06-1983 --date2 22-06-1983      ✔  Py395_default 
19 days elapsed

 ~/PycharmProjects/DateCalculator  ./DateCalculator.py --date1 04-07-1984 --date2 25-12-1984      ✔  Py395_default 
173 days elapsed

 ~/PycharmProjects/DateCalculator  ./DateCalculator.py --date1 03-01-1989 --date2 03-08-1983      ✔  Py395_default 
1979 days elapsed
"""
