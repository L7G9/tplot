from django.test import TestCase

from timelines.pdf.round import Round
from historical_timelines.historical_year import HistoricalYear


class AgeTest(TestCase):
    def test_round_year_up(self):
        year = HistoricalYear(7)
        year.round(5, Round.UP)
        self.assertEqual(year.year, 10)

    def test_round_negative_year_up(self):
        year = HistoricalYear(-7)
        year.round(5, Round.UP)
        self.assertEqual(year.year, -5)

    def test_round_year_down(self):
        year = HistoricalYear(7)
        year.round(5, Round.DOWN)
        self.assertEqual(year.year, 5)

    def test_round_year_months_down(self):
        year = HistoricalYear(-7)
        year.round(5, Round.DOWN)
        self.assertEqual(year.year, -10)

    def test_str_0(self):
        age_string = str(HistoricalYear(0))
        self.assertEqual(age_string, "BC/AD")

    def test_start_end_string_bc(self):
        age_string = HistoricalYear(-10).start_end_string(HistoricalYear(-5))
        self.assertEqual(age_string, "10 to 5 BC")

    def test_start_end_string_ad(self):
        age_string = HistoricalYear(5).start_end_string(HistoricalYear(10))
        self.assertEqual(age_string, "5 to 10 AD")

    def test_start_end_string_bc_to_ad(self):
        age_string = HistoricalYear(-5).start_end_string(HistoricalYear(10))
        self.assertEqual(age_string, "5 BC to 10 AD")

    def test_1y_lt_2y(self):
        result = HistoricalYear(1) < HistoricalYear(2)
        self.assertEqual(result, True)

    def test_1y_lt_1y(self):
        result = HistoricalYear(1) < HistoricalYear(1)
        self.assertEqual(result, False)

    def test_2y_lt_1y(self):
        result = HistoricalYear(2) < HistoricalYear(1)
        self.assertEqual(result, False)

    def test_1y_le_2y(self):
        result = HistoricalYear(1) <= HistoricalYear(2)
        self.assertEqual(result, True)

    def test_1y_le_1y(self):
        result = HistoricalYear(1) <= HistoricalYear(1)
        self.assertEqual(result, True)

    def test_2y_le_1y(self):
        result = HistoricalYear(2) <= HistoricalYear(1)
        self.assertEqual(result, False)

    def test_1y_eq_2y(self):
        result = HistoricalYear(1) == HistoricalYear(2)
        self.assertEqual(result, False)

    def test_1y_eq_1y(self):
        result = HistoricalYear(1) == HistoricalYear(1)
        self.assertEqual(result, True)

    def test_2y_eq_1y(self):
        result = HistoricalYear(2) == HistoricalYear(1)
        self.assertEqual(result, False)

    def test_1y_ne_2y(self):
        result = HistoricalYear(1) != HistoricalYear(2)
        self.assertEqual(result, True)

    def test_1y_ne_1y(self):
        result = HistoricalYear(1) != HistoricalYear(1)
        self.assertEqual(result, False)

    def test_2y_ne_1y(self):
        result = HistoricalYear(2) != HistoricalYear(1)
        self.assertEqual(result, True)

    def test_1y_gt_2y(self):
        result = HistoricalYear(1) > HistoricalYear(2)
        self.assertEqual(result, False)

    def test_1y_gt_1y(self):
        result = HistoricalYear(1) > HistoricalYear(1)
        self.assertEqual(result, False)

    def test_2y_gt_1y(self):
        result = HistoricalYear(2) > HistoricalYear(1)
        self.assertEqual(result, True)

    def test_1y_ge_2y(self):
        result = HistoricalYear(1) >= HistoricalYear(2)
        self.assertEqual(result, False)

    def test_1y_ge_1y(self):
        result = HistoricalYear(1) >= HistoricalYear(1)
        self.assertEqual(result, True)

    def test_2y_ge_1y(self):
        result = HistoricalYear(2) >= HistoricalYear(1)
        self.assertEqual(result, True)
