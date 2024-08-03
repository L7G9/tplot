from django.test import TestCase

from timelines.pdf.round import Round
from scientific_timelines.scientific_year import ScientificYear


class ScientificYearTest(TestCase):
    def test_round_year_up(self):
        year = ScientificYear(0.5, 1000)
        year.round(1000, Round.UP)
        self.assertEqual(year.fraction, 1)

    def test_round_year_down(self):
        year = ScientificYear(3.5, 1000)
        year.round(1000, Round.DOWN)
        self.assertEqual(year.fraction, 3)

    def test_change_multiplier_increase(self):
        year = ScientificYear(300, 1000)
        year.change_multiplier(1000000)
        self.assertEqual(year.fraction, 0.3)
        self.assertEqual(year.multiplier, 1000000)

    def test_change_multiplier_deacrease(self):
        year = ScientificYear(0.005, 1000000)
        year.change_multiplier(1000)
        self.assertEqual(year.fraction, 5)
        self.assertEqual(year.multiplier, 1000)

    def test_str_0(self):
        result = str(ScientificYear(0, 1000))
        self.assertEqual(result, "0 thousand years")

    def test_str_million_ago(self):
        result = str(ScientificYear(-0.5, 1000000))
        self.assertEqual(result, "0.5 million years ago")

    def test_str_billion_from_now(self):
        result = str(ScientificYear(1.5, 1000000000))
        self.assertEqual(result, "1.5 billion years from now")

    def test_start_end_string_similar(self):
        result = ScientificYear(10, 1000).start_end_string(
            ScientificYear(15, 1000)
        )
        self.assertEqual(result, "10 to 15 thousand years from now")

    def test_start_end_string_different(self):
        result = ScientificYear(-10, 1000).start_end_string(
            ScientificYear(15, 1000)
        )
        self.assertEqual(
            result, "10 thousand years ago to 15 thousand years from now"
        )

    def test_1y_lt_2y(self):
        result = ScientificYear(1, 1000) < ScientificYear(2, 1000)
        self.assertEqual(result, True)

    def test_1y_lt_1y(self):
        result = ScientificYear(1, 1000) < ScientificYear(1, 1000)
        self.assertEqual(result, False)

    def test_2y_lt_1y(self):
        result = ScientificYear(2, 1000) < ScientificYear(1, 1000)
        self.assertEqual(result, False)

    def test_1y_le_2y(self):
        result = ScientificYear(1, 1000) <= ScientificYear(2, 1000)
        self.assertEqual(result, True)

    def test_1y_le_1y(self):
        result = ScientificYear(1, 1000) <= ScientificYear(1, 1000)
        self.assertEqual(result, True)

    def test_2y_le_1y(self):
        result = ScientificYear(2, 1000) <= ScientificYear(1, 1000)
        self.assertEqual(result, False)

    def test_1y_eq_2y(self):
        result = ScientificYear(1, 1000) == ScientificYear(2, 1000)
        self.assertEqual(result, False)

    def test_1y_eq_1y(self):
        result = ScientificYear(1, 1000) == ScientificYear(1, 1000)
        self.assertEqual(result, True)

    def test_2y_eq_1y(self):
        result = ScientificYear(2, 1000) == ScientificYear(1, 1000)
        self.assertEqual(result, False)

    def test_1y_ne_2y(self):
        result = ScientificYear(1, 1000) != ScientificYear(2, 1000)
        self.assertEqual(result, True)

    def test_1y_ne_1y(self):
        result = ScientificYear(1, 1000) != ScientificYear(1, 1000)
        self.assertEqual(result, False)

    def test_2y_ne_1y(self):
        result = ScientificYear(2, 1000) != ScientificYear(1, 1000)
        self.assertEqual(result, True)

    def test_1y_gt_2y(self):
        result = ScientificYear(1, 1000) > ScientificYear(2, 1000)
        self.assertEqual(result, False)

    def test_1y_gt_1y(self):
        result = ScientificYear(1, 1000) > ScientificYear(1, 1000)
        self.assertEqual(result, False)

    def test_2y_gt_1y(self):
        result = ScientificYear(2, 1000) > ScientificYear(1, 1000)
        self.assertEqual(result, True)

    def test_1y_ge_2y(self):
        result = ScientificYear(1, 1000) >= ScientificYear(2, 1000)
        self.assertEqual(result, False)

    def test_1y_ge_1y(self):
        result = ScientificYear(1, 1000) >= ScientificYear(1, 1000)
        self.assertEqual(result, True)

    def test_2y_ge_1y(self):
        result = ScientificYear(2, 1000) >= ScientificYear(1, 1000)
        self.assertEqual(result, True)
