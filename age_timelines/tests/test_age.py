from django.test import TestCase

from timelines.pdf.round import Round
from age_timelines.pdf.age import Age


class AgeTest(TestCase):
    def test_round_months_up(self):
        age = Age(1, 1)
        age.round_months(Round.UP)
        self.assertEqual(age.years, 2)
        self.assertEqual(age.months, 0)

    def test_round_negative_months_up(self):
        age = Age(1, -1)
        age.round_months(Round.UP)
        self.assertEqual(age.years, 1)
        self.assertEqual(age.months, 0)

    def test_round_months_down(self):
        age = Age(1, 1)
        age.round_months(Round.DOWN)
        self.assertEqual(age.years, 1)
        self.assertEqual(age.months, 0)

    def test_round_negative_months_down(self):
        age = Age(1, -1)
        age.round_months(Round.DOWN)
        self.assertEqual(age.years, 0)
        self.assertEqual(age.months, 0)

    def test_round_years_up(self):
        age = Age(7, 0)
        age.round_years(5, Round.UP)
        self.assertEqual(age.years, 10)

    def test_round_negative_years_up(self):
        age = Age(-7, 0)
        age.round_years(5, Round.UP)
        self.assertEqual(age.years, -5)

    def test_round_years_down(self):
        age = Age(7, 0)
        age.round_years(5, Round.DOWN)
        self.assertEqual(age.years, 5)

    def test_round_years_months_down(self):
        age = Age(-7, 0)
        age.round_years(5, Round.DOWN)
        self.assertEqual(age.years, -10)

    def test_str_months(self):
        age_string = str(Age(0, 6))
        self.assertEqual(age_string, "6 Months")

    def test_str_years(self):
        age_string = str(Age(6, 0))
        self.assertEqual(age_string, "6 Years")

    def test_str_years_and_months(self):
        age_string = str(Age(6, 6))
        self.assertEqual(age_string, "6 Years 6 Months")

    def test_add(self):
        age = Age(4, 0) + Age(2, 6)
        self.assertEqual(age.years, 6)
        self.assertEqual(age.months, 6)

    def test_sub(self):
        age = Age(4, 0) - Age(2, 6)
        self.assertEqual(age.years, 2)
        self.assertEqual(age.months, -6)

    def test_iadd(self):
        age = Age(4, 0)
        age += Age(2, 6)
        self.assertEqual(age.years, 6)
        self.assertEqual(age.months, 6)

    def test_isub(self):
        age = Age(4, 0)
        age -= Age(2, 6)
        self.assertEqual(age.years, 2)
        self.assertEqual(age.months, -6)

    def test_1y_lt_2y(self):
        result = Age(1, 0) < Age(2, 0)
        self.assertEqual(result, True)

    def test_1y_lt_12m(self):
        result = Age(1, 0) < Age(0, 12)
        self.assertEqual(result, False)

    def test_2y_lt_1y(self):
        result = Age(2, 0) < Age(1, 0)
        self.assertEqual(result, False)

    def test_1y_le_2y(self):
        result = Age(1, 0) <= Age(2, 0)
        self.assertEqual(result, True)

    def test_1y_le_12m(self):
        result = Age(1, 0) <= Age(0, 12)
        self.assertEqual(result, True)

    def test_2y_le_1y(self):
        result = Age(2, 0) <= Age(1, 0)
        self.assertEqual(result, False)

    def test_1y_eq_2y(self):
        result = Age(1, 0) == Age(2, 0)
        self.assertEqual(result, False)

    def test_1y_eq_12m(self):
        result = Age(1, 0) == Age(0, 12)
        self.assertEqual(result, True)

    def test_2y_eq_1y(self):
        result = Age(2, 0) == Age(1, 0)
        self.assertEqual(result, False)

    def test_1y_ne_2y(self):
        result = Age(1, 0) != Age(2, 0)
        self.assertEqual(result, True)

    def test_1y_ne_12m(self):
        result = Age(1, 0) != Age(0, 12)
        self.assertEqual(result, False)

    def test_2y_ne_1y(self):
        result = Age(2, 0) != Age(1, 0)
        self.assertEqual(result, True)

    def test_1y_gt_2y(self):
        result = Age(1, 0) > Age(2, 0)
        self.assertEqual(result, False)

    def test_1y_gt_12m(self):
        result = Age(1, 0) > Age(0, 12)
        self.assertEqual(result, False)

    def test_2y_gt_1y(self):
        result = Age(2, 0) > Age(1, 0)
        self.assertEqual(result, True)

    def test_1y_ge_2y(self):
        result = Age(1, 0) >= Age(2, 0)
        self.assertEqual(result, False)

    def test_1y_ge_12m(self):
        result = Age(1, 0) >= Age(0, 12)
        self.assertEqual(result, True)

    def test_2y_ge_1y(self):
        result = Age(2, 0) >= Age(1, 0)
        self.assertEqual(result, True)
