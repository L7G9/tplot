from datetime import datetime
from django.test import TestCase

from date_time_timelines.models import (
    WEEK_1,
    MONTH_1,
    MONTH_2,
    MONTH_3,
    MONTH_6,
    YEAR_1,
    YEAR_5,
    YEAR_10,
    YEAR_100,
    YEAR_1000
)
from timelines.pdf.round import Round
from date_time_timelines.pdf.datetime import (
    DateTime,
    round_datetime,
    round_by_seconds,
    round_by_weeks,
    round_by_months,
    round_by_years,
    is_week_scale_unit,
    is_month_scale_unit,
    is_year_scale_unit,
    get_months_in_scale_unit,
    get_years_in_scale_unit
)


class DateTimeTest(TestCase):
    def test_round_by_seconds_up_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        result = round_by_seconds(date_time, 5, Round.UP)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_seconds_up_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=1
        )
        result = round_by_seconds(date_time, 5, Round.UP)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=5
        )
        self.assertEqual(result, expected)

    def test_round_by_seconds_down_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        result = round_by_seconds(date_time, 5, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_seconds_down_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=1
        )
        result = round_by_seconds(date_time, 5, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_minutes_up_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=30, second=0
        )
        result = round_by_seconds(date_time, 5*60, Round.UP)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=30, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_minutes_up_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=28, second=5
        )
        result = round_by_seconds(date_time, 5*60, Round.UP)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=30, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_minutes_down_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=30, second=0
        )
        result = round_by_seconds(date_time, 5*60, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=30, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_minutes_down_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=28, second=5
        )
        result = round_by_seconds(date_time, 5*60, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=25, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_hours_up_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=12, minute=0, second=0
        )
        result = round_by_seconds(date_time, 3*60*60, Round.UP)
        expected = datetime(
            year=2000, month=1, day=1, hour=12, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_hours_up_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=12, minute=0, second=30
        )
        result = round_by_seconds(date_time, 3*60*60, Round.UP)
        expected = datetime(
            year=2000, month=1, day=1, hour=15, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_hours_down_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=12, minute=0, second=0
        )
        result = round_by_seconds(date_time, 3*60*60, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=12, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_hours_down_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=12, minute=0, second=30
        )
        result = round_by_seconds(date_time, 3*60*60, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=12, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_days_up_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=5, hour=0, minute=0, second=0
        )
        result = round_by_seconds(date_time, 24*60*60, Round.UP)
        expected = datetime(
            year=2000, month=1, day=5, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_days_up_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=5, hour=0, minute=0, second=5
        )
        result = round_by_seconds(date_time, 24*60*60, Round.UP)
        expected = datetime(
            year=2000, month=1, day=6, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_days_down_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=5, hour=0, minute=0, second=0
        )
        result = round_by_seconds(date_time, 24*60*60, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=5, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_days_down_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=5, hour=18, minute=45, second=5
        )
        result = round_by_seconds(date_time, 24*60*60, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=5, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_weeks_up_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=3, hour=0, minute=0, second=0
        )
        result = round_by_weeks(date_time, Round.UP)
        expected = datetime(
            year=2000, month=1, day=3, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_weeks_up_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=3, hour=0, minute=0, second=5
        )
        result = round_by_weeks(date_time, Round.UP)
        expected = datetime(
            year=2000, month=1, day=10, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_weeks_down_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=3, hour=0, minute=0, second=0
        )
        result = round_by_weeks(date_time, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=3, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_weeks_down_rounding_required(self):
        date_time = datetime(
            year=2000, month=1, day=5, hour=18, minute=45, second=5
        )
        result = round_by_weeks(date_time, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=3, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_is_week_scale_unit_true(self):
        self.assertTrue(is_week_scale_unit(WEEK_1))

    def test_is_week_scale_unit_false(self):
        self.assertFalse(is_week_scale_unit(MONTH_1))

    def test_round_by_months_up_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=7, day=1, hour=0, minute=0, second=0
        )
        result = round_by_months(date_time, 6, Round.UP)
        expected = datetime(
            year=2000, month=7, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_months_up_rounding_required(self):
        date_time = datetime(
            year=2000, month=6, day=5, hour=18, minute=45, second=5
        )
        result = round_by_months(date_time, 6, Round.UP)
        expected = datetime(
            year=2000, month=7, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_months_down_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=7, day=1, hour=0, minute=0, second=0
        )
        result = round_by_months(date_time, 6, Round.DOWN)
        expected = datetime(
            year=2000, month=7, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_months_down_rounding_required(self):
        date_time = datetime(
            year=2000, month=6, day=5, hour=18, minute=45, second=5
        )
        result = round_by_months(date_time, 6, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_is_month_scale_unit_1(self):
        self.assertTrue(is_month_scale_unit(MONTH_1))

    def test_is_month_scale_unit_2(self):
        self.assertTrue(is_month_scale_unit(MONTH_2))

    def test_is_month_scale_unit_3(self):
        self.assertTrue(is_month_scale_unit(MONTH_3))

    def test_is_month_scale_unit_6(self):
        self.assertTrue(is_month_scale_unit(MONTH_6))

    def test_is_month_scale_unit_false(self):
        self.assertFalse(is_month_scale_unit(YEAR_1))

    def test_get_months_in_scale_unit_1(self):
        self.assertEqual(get_months_in_scale_unit(MONTH_1), 1)

    def test_get_months_in_scale_unit_2(self):
        self.assertEqual(get_months_in_scale_unit(MONTH_2), 2)

    def test_get_months_in_scale_unit_3(self):
        self.assertEqual(get_months_in_scale_unit(MONTH_3), 3)

    def test_get_months_in_scale_unit_6(self):
        self.assertEqual(get_months_in_scale_unit(MONTH_6), 6)

    def test_round_by_years_up_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        result = round_by_years(date_time, 5, Round.UP)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_years_up_rounding_required(self):
        date_time = datetime(
            year=2000, month=6, day=5, hour=18, minute=45, second=5
        )
        result = round_by_years(date_time, 5, Round.UP)
        expected = datetime(
            year=2005, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_years_down_rounding_not_required(self):
        date_time = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        result = round_by_years(date_time, 5, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_round_by_years_down_rounding_required(self):
        date_time = datetime(
            year=2003, month=6, day=5, hour=18, minute=45, second=5
        )
        result = round_by_years(date_time, 5, Round.DOWN)
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_is_year_scale_unit_1(self):
        self.assertTrue(is_year_scale_unit(YEAR_1))

    def test_is_year_scale_unit_5(self):
        self.assertTrue(is_year_scale_unit(YEAR_5))

    def test_is_year_scale_unit_10(self):
        self.assertTrue(is_year_scale_unit(YEAR_10))

    def test_is_year_scale_unit_100(self):
        self.assertTrue(is_year_scale_unit(YEAR_100))

    def test_is_year_scale_unit_1000(self):
        self.assertTrue(is_year_scale_unit(YEAR_1000))

    def test_is_year_scale_unit_false(self):
        self.assertFalse(is_year_scale_unit(MONTH_1))

    def test_get_years_in_scale_unit_1(self):
        self.assertEqual(get_years_in_scale_unit(YEAR_1), 1)

    def test_get_years_in_scale_unit_5(self):
        self.assertEqual(get_years_in_scale_unit(YEAR_5), 5)

    def test_get_years_in_scale_unit_10(self):
        self.assertEqual(get_years_in_scale_unit(YEAR_10), 10)

    def test_get_years_in_scale_unit_100(self):
        self.assertEqual(get_years_in_scale_unit(YEAR_100), 100)

    def test_get_years_in_scale_unit_1000(self):
        self.assertEqual(get_years_in_scale_unit(YEAR_1000), 1000)

    def test_round_weeks(self):
        input = datetime(year=2000, month=2, day=2)
        result = round_datetime(input, WEEK_1, Round.DOWN)
        expected = datetime(year=2000, month=1, day=31)
        self.assertEqual(result, expected)

    def test_round_months(self):
        input = datetime(year=2000, month=3, day=1)
        result = round_datetime(input, MONTH_3, Round.DOWN)
        expected = datetime(year=2000, month=1, day=1)
        self.assertEqual(result, expected)

    def test_round_years(self):
        input = datetime(year=2015, month=1, day=1)
        result = round_datetime(input, YEAR_10, Round.DOWN)
        expected = datetime(year=2010, month=1, day=1)
        self.assertEqual(result, expected)

    def test_round_seconds(self):
        input = datetime(year=2000, month=1, day=1, hour=0, minute=0, second=43)
        result = round_datetime(input, 5, Round.DOWN)
        expected = datetime(year=2000, month=1, day=1, second=40)
        self.assertEqual(result, expected)

    def test_datetime_round(self):
        result = DateTime(datetime(year=2015, month=1, day=1))
        result.round_to_scale_unit(YEAR_10, Round.DOWN)
        expected = datetime(year=2010, month=1, day=1)
        self.assertEqual(result.date_time, expected)
