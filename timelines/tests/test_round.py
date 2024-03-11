from django.test import TestCase

from timelines.pdf.round import Round


class TestRound(TestCase):
    def test_up(self):
        round = Round.UP
        self.assertTrue(round.up())
        self.assertFalse(round.down())

    def test_down(self):
        round = Round.DOWN
        self.assertTrue(round.down())
        self.assertFalse(round.up())
