import io

from django.contrib.auth.models import User
from django.test import TestCase
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from age_timelines.models import AgeEvent, AgeTimeline
from age_timelines.pdf.age_timeline_scale_description import \
    AgeTimelineScaleDescription
from timelines.pdf.pdf_scale_line import PDFScaleLine

UNIT_LINE_LENGTH = 5 * mm


class TestPDFScaleLine(TestCase):
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

    def test_landscape(self):
        scale_line = PDFScaleLine(
            self.landscape_scale_description,
            self.__create_canvas(),
            UNIT_LINE_LENGTH,
        )

        expected_width = (
            self.landscape_scale_description.get_scale_length() * mm
        )
        expected_height = UNIT_LINE_LENGTH
        self.assertEqual(scale_line.width, expected_width)
        self.assertEqual(scale_line.height, expected_height)

    def test_portrait(self):
        scale_line = PDFScaleLine(
            self.portrait_scale_description,
            self.__create_canvas(),
            UNIT_LINE_LENGTH,
        )

        expected_width = UNIT_LINE_LENGTH
        expected_height = (
            self.portrait_scale_description.get_scale_length() * mm
        )
        self.assertEqual(scale_line.width, expected_width)
        self.assertEqual(scale_line.height, expected_height)
