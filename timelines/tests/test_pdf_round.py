from django.contrib.auth.models import User
from django.test import TestCase

from timelines.pdf.round import Round

class RoundTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.round_up = Round.UP
        self.round_down = Round.DOWN

    def test_round_up_is_up(self):
        is_up = self.round_up.up()
        self.assertEqual(is_up, True)

    def test_round_up_is_down(self):
        is_down = self.round_up.down()
        self.assertEqual(is_down, False)

    def test_round_down_is_up(self):
        is_up = self.round_down.up()
        self.assertEqual(is_up, False)

    def test_round_down_is_down(self):
        is_down = self.round_down.down()
        self.assertEqual(is_down, True)
