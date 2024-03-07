from django.test import TestCase

from timelines.pdf.area import Area
from timelines.pdf.pdf_event import PDFEventEmpty
from timelines.pdf.pdf_event_area import PDFEventArea


class PDFEventAreaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pdf_event_area_landscape = PDFEventArea(
            0,
            0,
            160,
            80,
            None
        )
        cls.pdf_event_area_landscape.events.append(
            PDFEventEmpty(40, 0, 20, 20)
        )
        cls.pdf_event_area_landscape.events.append(
            PDFEventEmpty(70, 0, 30, 60)
        )

    def test_landscape_position_event(self):
        test_area = Area(10, 0, 20, 30)
        position = self.pdf_event_area_landscape.get_landscape_position(
            test_area,
            True,
            True,
            None,
            5
        )
        self.assertIsNotNone(position)
        self.assertEqual(position[0], 10)
        self.assertEqual(position[1], 0)

    def test_landscape_position_above_event(self):
        test_area = Area(40, 0, 20, 20)
        position = self.pdf_event_area_landscape.get_landscape_position(
            test_area,
            True,
            True,
            None,
            5
        )
        self.assertIsNotNone(position)
        self.assertEqual(position[0], 40)
        self.assertEqual(position[1], 25)

    def test_landscape_position_left_and_above_event(self):
        test_area = Area(60, 0, 30, 30)
        position = self.pdf_event_area_landscape.get_landscape_position(
            test_area,
            True,
            True,
            None,
            5
        )
        self.assertIsNotNone(position)
        self.assertEqual(position[0], 35)
        self.assertEqual(position[1], 25)

    def test_landscape_position_right_of_event(self):
        test_area = Area(80, 0, 30, 30)
        position = self.pdf_event_area_landscape.get_landscape_position(
            test_area,
            True,
            True,
            None,
            5
        )
        self.assertIsNotNone(position)
        self.assertEqual(position[0], 105)
        self.assertEqual(position[1], 0)

    def test_landscape_position_off_right_edge(self):
        test_area = Area(140, 0, 30, 30)
        position = self.pdf_event_area_landscape.get_landscape_position(
            test_area,
            True,
            True,
            None,
            5
        )
        self.assertIsNotNone(position)
        self.assertEqual(position[0], 140)
        self.assertEqual(position[1], 0)

    def test_landscape_too_big(self):
        test_area = Area(0, 0, 30, 90)
        position = self.pdf_event_area_landscape.get_landscape_position(
            test_area,
            True,
            True,
            None,
            5
        )
        self.assertIsNone(position)
