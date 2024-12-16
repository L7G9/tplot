import io

from django.contrib.auth.models import User
from django.test import TestCase
from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from age_timelines.models import AgeEvent, AgeTimeline
from age_timelines.pdf.age_timeline_scale_description import (
    AgeTimelineScaleDescription,
)
from timelines.pdf.pdf_scale import PDFScale


class TestPDFScale(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        landscape_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=5,
            scale_unit_length=5,
            page_size="4",
            page_orientation="L",
            page_scale_position=1,
        )

        AgeEvent.objects.create(
            age_timeline=landscape_timeline,
            timeline_id=landscape_timeline.timeline_ptr.pk,
            title="Start Age Event",
            start_year=1,
            start_month=0,
            has_end=False,
        )

        AgeEvent.objects.create(
            age_timeline=landscape_timeline,
            timeline_id=landscape_timeline.timeline_ptr.pk,
            title="End Age Event",
            start_year=24,
            start_month=0,
            has_end=False,
        )

        cls.landscape_scale_description = AgeTimelineScaleDescription(
            landscape_timeline
        )

        portrait_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=1,
            scale_unit_length=10,
            page_size="4",
            page_orientation="P",
            page_scale_position=1,
        )

        AgeEvent.objects.create(
            age_timeline=portrait_timeline,
            timeline_id=portrait_timeline.timeline_ptr.pk,
            title="Start Age Event",
            start_year=10,
            start_month=0,
            has_end=False,
        )

        AgeEvent.objects.create(
            age_timeline=portrait_timeline,
            timeline_id=portrait_timeline.timeline_ptr.pk,
            title="End Age Event",
            start_year=18,
            start_month=0,
            has_end=True,
            end_year=22,
            end_month=0,
        )

        cls.portrait_scale_description = AgeTimelineScaleDescription(
            portrait_timeline
        )

    def __create_canvas(self) -> Canvas:
        buffer = io.BytesIO()
        canvas = Canvas(
            buffer,
            pagesize=(210 * mm, 297 * mm),
        )
        canvas.setStrokeColorRGB(0, 0, 0)
        return canvas

    def __create_paragraph_style(self):
        return ParagraphStyle(
            "Basic Text ParagraphStyle",
            fontName="Times-Roman",
            fontSize=10,
            borderColor=black,
            borderWidth=0,
            leading=14,
        )

    def test_landscape(self):
        scale = PDFScale(
            self.landscape_scale_description,
            self.__create_canvas(),
            self.__create_paragraph_style(),
        )
        expected_width = scale.units.width
        expected_height = scale.units.height + scale.line.height

        self.assertEqual(scale.width, expected_width)
        self.assertEqual(scale.height, expected_height)

    def test_landscape_move(self):
        scale = PDFScale(
            self.landscape_scale_description,
            self.__create_canvas(),
            self.__create_paragraph_style(),
        )
        x = 10 * mm
        y = 20 * mm
        scale.move(x, y)

        expected_x = x
        expected_y = y
        expected_units_x = x
        expected_units_y = y
        expected_line_x = x + scale.units.start_offset
        expected_line_y = y + scale.units.height

        self.assertEqual(scale.x, expected_x)
        self.assertEqual(scale.y, expected_y)
        self.assertEqual(scale.units.x, expected_units_x)
        self.assertEqual(scale.units.y, expected_units_y)
        self.assertEqual(scale.line.x, expected_line_x)
        self.assertEqual(scale.line.y, expected_line_y)

    def test_portrait(self):
        scale = PDFScale(
            self.portrait_scale_description,
            self.__create_canvas(),
            self.__create_paragraph_style(),
        )
        expected_width = scale.units.width + scale.line.width
        expected_height = scale.units.height

        self.assertEqual(scale.width, expected_width)
        self.assertEqual(scale.height, expected_height)

    def test_portrait_move(self):
        scale = PDFScale(
            self.portrait_scale_description,
            self.__create_canvas(),
            self.__create_paragraph_style(),
        )
        x = 10 * mm
        y = 20 * mm
        scale.move(x, y)

        expected_x = x
        expected_y = y
        expected_units_x = x
        expected_units_y = y
        expected_line_x = x + scale.units.width
        expected_line_y = y + scale.units.start_offset

        self.assertEqual(scale.x, expected_x)
        self.assertEqual(scale.y, expected_y)
        self.assertEqual(scale.units.x, expected_units_x)
        self.assertEqual(scale.units.y, expected_units_y)
        self.assertEqual(scale.line.x, expected_line_x)
        self.assertEqual(scale.line.y, expected_line_y)
