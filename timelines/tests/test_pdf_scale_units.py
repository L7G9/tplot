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
from timelines.pdf.pdf_scale_units import PDFScaleUnits


class TestPDFScaleUnits(TestCase):
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
            scale_length=5,
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
            scale_length=10,
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
        scale_units = PDFScaleUnits(
            self.landscape_scale_description,
            self.__create_paragraph_style(),
            self.__create_canvas(),
        )

        expected_labels = (
            self.landscape_scale_description.get_scale_units() + 1
        )
        expected_width = (
            self.landscape_scale_description.get_scale_length() * mm
            + scale_units.unit_labels[0].width / 2
            + scale_units.unit_labels[-1].width / 2
        )
        expected_offset = scale_units.unit_labels[0].width / 2

        self.assertEqual(len(scale_units.unit_labels), expected_labels)
        self.assertEqual(scale_units.width, expected_width)
        self.assertEqual(scale_units.start_offset, expected_offset)

    def test_portrait(self):
        scale_units = PDFScaleUnits(
            self.portrait_scale_description,
            self.__create_paragraph_style(),
            self.__create_canvas(),
        )

        expected_labels = self.portrait_scale_description.get_scale_units() + 1
        expected_height = (
            self.portrait_scale_description.get_scale_length() * mm
            + scale_units.unit_labels[0].height / 2
            + scale_units.unit_labels[-1].height / 2
        )
        expected_offset = scale_units.unit_labels[0].height / 2

        self.assertEqual(len(scale_units.unit_labels), expected_labels)
        self.assertEqual(scale_units.height, expected_height)
        self.assertEqual(scale_units.start_offset, expected_offset)
