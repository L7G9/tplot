from datetime import datetime
from django.test import TestCase

from timelines.pdf.round import Round
from date_time_timelines.pdf.datetime_utls import (
    round_by_seconds,
    round_by_weeks,
    round_by_months,
    round_by_years,
    get_start_of_month,
    get_start_of_next_month,
    seconds_between,
    get_month_completion
)


class DateTimeUtlsTest(TestCase):
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

    def test_get_start_of_month_at_start(self):
        input = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=0
        )
        result = get_start_of_month(input)
        expected = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_get_start_of_month_days_over(self):
        input = datetime(
            year=2000, month=11, day=4, hour=0, minute=0, second=0
        )
        result = get_start_of_month(input)
        expected = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_get_start_of_month_seconds_over(self):
        input = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=1
        )
        result = get_start_of_month(input)
        expected = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_get_start_of_next_month_at_start(self):
        input = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=0
        )
        result = get_start_of_next_month(input)
        expected = datetime(
            year=2000, month=12, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_get_start_of_next_month_days_over(self):
        input = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=0
        )
        result = get_start_of_next_month(input)
        expected = datetime(
            year=2000, month=12, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_get_start_of_next_month_seconds_over(self):
        input = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=0
        )
        result = get_start_of_next_month(input)
        expected = datetime(
            year=2000, month=12, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_get_start_of_next_month_dec_to_jan(self):
        input = datetime(
            year=2000, month=12, day=15, hour=0, minute=0, second=0
        )
        result = get_start_of_next_month(input)
        expected = datetime(
            year=2001, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_seconds_between_same(self):
        from_date = datetime(
            year=2000, month=11, day=16, hour=0, minute=0, second=0
        )
        to_date = datetime(
            year=2000, month=11, day=16, hour=0, minute=0, second=0
        )
        result = seconds_between(from_date, to_date)
        self.assertEqual(result, 0)

    def test_seconds_between_smaller(self):
        from_date = datetime(
            year=2000, month=11, day=16, hour=0, minute=0, second=0
        )
        to_date = datetime(
            year=2000, month=11, day=16, hour=0, minute=1, second=0
        )
        result = seconds_between(from_date, to_date)
        self.assertEqual(result, 60)

    def test_seconds_between_larger(self):
        from_date = datetime(
            year=2000, month=11, day=16, hour=0, minute=1, second=0
        )
        to_date = datetime(
            year=2000, month=11, day=16, hour=0, minute=0, second=0
        )
        result = seconds_between(from_date, to_date)
        self.assertEqual(result, -60)

    def test_get_month_completion_0(self):
        input = datetime(
            year=2000, month=11, day=1, hour=0, minute=0, second=0
        )
        result = get_month_completion(input)
        self.assertEqual(result, 0)

    def test_get_month_completion_50(self):
        input = datetime(
            year=2000, month=11, day=16, hour=0, minute=0, second=0
        )
        result = get_month_completion(input)
        self.assertEqual(result, 0.5)

    def test_get_month_completion_75(self):
        input = datetime(
            year=2000, month=11, day=23, hour=12, minute=0, second=0
        )
        result = get_month_completion(input)
        self.assertAlmostEqual(result, 0.75)
