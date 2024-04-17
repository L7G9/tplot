from datetime import datetime
from django.test import TestCase

from date_time_timelines.pdf.date_time import DateTime


class DateTimeTest(TestCase):
    def test_years(self):
        date_time = DateTime(datetime(year=2000, month=1, day=1))
        result = date_time.years()
        self.assertEqual(result, 1999)

    def test_months(self):
        date_time = DateTime(datetime(year=2000, month=12, day=1))
        result = date_time.months()
        self.assertEqual(result, 23999)

    def test_seconds(self):
        date_time = DateTime(
            datetime(year=1970, month=1, day=1, hour=0, minute=30, second=5)
        )
        result = date_time.seconds()
        self.assertEqual(result, 1805)
