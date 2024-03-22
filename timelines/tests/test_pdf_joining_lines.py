from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeEvent, AgeTimeline
from age_timelines.pdf.pdf_age_timeline import PDFAgeTimeline
from timelines.models import EventArea


class PDFJoiningLinesLandscapeTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        self.age_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=5,
            scale_length=5,
            page_size="4",
            page_orientation="L",
            page_scale_position=1,
        )
        self.before_event_area = EventArea.objects.create(
            timeline=self.age_timeline.timeline_ptr,
            name="Event Area before scale",
            page_position=0,
            weight=1,
        )
        self.after_event_area = EventArea.objects.create(
            timeline=self.age_timeline.timeline_ptr,
            name="Event Area after scale",
            page_position=1,
            weight=1,
        )

        self.before_event = AgeEvent.objects.create(
            age_timeline=self.age_timeline,
            timeline_id=self.age_timeline.timeline_ptr.pk,
            title="Before Age Event",
            start_year=5,
            start_month=0,
            has_end=False,
            event_area=self.before_event_area
        )

        self.after_event = AgeEvent.objects.create(
            age_timeline=self.age_timeline,
            timeline_id=self.age_timeline.timeline_ptr.pk,
            title="After Age Event",
            start_year=10,
            start_month=0,
            has_end=False,
            event_area=self.after_event_area
        )

    def test_init(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        layout = pdf_age_timeline.layout
        joining_lines = pdf_age_timeline.joining_lines
        self.assertEqual(joining_lines.x, layout.drawable_area.x)
        self.assertEqual(joining_lines.y, layout.drawable_area.y)
        self.assertEqual(joining_lines.width, layout.drawable_area.width)
        self.assertEqual(joining_lines.height, layout.drawable_area.height)

    def test_is_before_event_area_left_of_scale(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        joining_lines = pdf_age_timeline.joining_lines
        result = joining_lines.is_before(
            self.before_event_area,
            pdf_age_timeline.timeline
        )
        self.assertTrue(result)

    def test_is_before_event_area_right_of_scale(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        joining_lines = pdf_age_timeline.joining_lines
        result = joining_lines.is_before(
            self.after_event_area,
            pdf_age_timeline.timeline
        )
        self.assertFalse(result)

    def test_get_line_event_left_of_scale(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        joining_lines = pdf_age_timeline.joining_lines
        pdf_event_area = pdf_age_timeline.layout.event_areas[0]
        pdf_event = pdf_event_area.events[0]
        pdf_scale = pdf_age_timeline.scale
        line = joining_lines.get_line(
            pdf_event_area,
            pdf_event,
            pdf_scale,
            "L",
            True
        )

        expected_x1 = pdf_event_area.x + pdf_event.x - joining_lines.x
        expected_y1 = pdf_event_area.y + pdf_event.top() - joining_lines.y
        expected_x2 = (
            pdf_scale.x + pdf_event.position_on_scale - joining_lines.x
        )
        expected_y2 = pdf_scale.y - joining_lines.y
        self.assertEqual(line.x1, expected_x1)
        self.assertEqual(line.y1, expected_y1)
        self.assertEqual(line.x2, expected_x2)
        self.assertEqual(line.y2, expected_y2)

    def test_get_line_event_right_of_scale(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        joining_lines = pdf_age_timeline.joining_lines
        pdf_event_area = pdf_age_timeline.layout.event_areas[1]
        pdf_event = pdf_event_area.events[0]
        pdf_scale = pdf_age_timeline.scale
        line = joining_lines.get_line(
            pdf_event_area,
            pdf_event,
            pdf_scale,
            "L",
            False
        )

        expected_x1 = pdf_event_area.x + pdf_event.x - joining_lines.x
        expected_y1 = pdf_event_area.y + pdf_event.y - joining_lines.y
        expected_x2 = (
            pdf_scale.x + pdf_event.position_on_scale - joining_lines.x
        )
        expected_y2 = pdf_scale.top() - joining_lines.y

        self.assertEqual(line.x1, expected_x1)
        self.assertEqual(line.y1, expected_y1)
        self.assertEqual(line.x2, expected_x2)
        self.assertEqual(line.y2, expected_y2)


class PDFJoiningLinesPortraitTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        self.age_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=5,
            scale_length=5,
            page_size="4",
            page_orientation="P",
            page_scale_position=1,
        )
        self.before_event_area = EventArea.objects.create(
            timeline=self.age_timeline.timeline_ptr,
            name="Event Area before scale",
            page_position=0,
            weight=1,
        )
        self.after_event_area = EventArea.objects.create(
            timeline=self.age_timeline.timeline_ptr,
            name="Event Area after scale",
            page_position=1,
            weight=1,
        )

        self.before_event = AgeEvent.objects.create(
            age_timeline=self.age_timeline,
            timeline_id=self.age_timeline.timeline_ptr.pk,
            title="Before Age Event",
            start_year=5,
            start_month=0,
            has_end=False,
            event_area=self.before_event_area
        )

        self.after_event = AgeEvent.objects.create(
            age_timeline=self.age_timeline,
            timeline_id=self.age_timeline.timeline_ptr.pk,
            title="After Age Event",
            start_year=10,
            start_month=0,
            has_end=False,
            event_area=self.after_event_area
        )

    def test_init(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        layout = pdf_age_timeline.layout
        joining_lines = pdf_age_timeline.joining_lines
        self.assertEqual(joining_lines.x, layout.drawable_area.x)
        self.assertEqual(joining_lines.y, layout.drawable_area.y)
        self.assertEqual(joining_lines.width, layout.drawable_area.width)
        self.assertEqual(joining_lines.height, layout.drawable_area.height)

    def test_is_before_event_area_below_scale(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        joining_lines = pdf_age_timeline.joining_lines
        result = joining_lines.is_before(
            self.before_event_area,
            pdf_age_timeline.timeline
        )
        self.assertTrue(result)

    def test_is_before_event_area_above_scale(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        joining_lines = pdf_age_timeline.joining_lines
        result = joining_lines.is_before(
            self.after_event_area,
            pdf_age_timeline.timeline
        )
        self.assertFalse(result)

    def test_get_line_event_below_scale(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        joining_lines = pdf_age_timeline.joining_lines
        pdf_event_area = pdf_age_timeline.layout.event_areas[0]
        pdf_event = pdf_event_area.events[0]
        pdf_scale = pdf_age_timeline.scale
        line = joining_lines.get_line(
            pdf_event_area,
            pdf_event,
            pdf_scale,
            "P",
            True
        )

        expected_x1 = pdf_event_area.x + pdf_event.right() - joining_lines.x
        expected_y1 = pdf_event_area.y + pdf_event.top() - joining_lines.y
        expected_x2 = pdf_scale.x - joining_lines.x
        expected_y2 = (
                pdf_scale.y
                + pdf_event.position_on_scale
                + pdf_event.height
                - joining_lines.y
        )
        self.assertEqual(line.x1, expected_x1)
        self.assertEqual(line.y1, expected_y1)
        self.assertEqual(line.x2, expected_x2)
        self.assertEqual(line.y2, expected_y2)

    def test_get_line_event_above_scale(self):
        pdf_age_timeline = PDFAgeTimeline(self.age_timeline)
        joining_lines = pdf_age_timeline.joining_lines
        pdf_event_area = pdf_age_timeline.layout.event_areas[1]
        pdf_event = pdf_event_area.events[0]
        pdf_scale = pdf_age_timeline.scale
        line = joining_lines.get_line(
            pdf_event_area,
            pdf_event,
            pdf_scale,
            "P",
            False
        )

        expected_x1 = pdf_event_area.x + pdf_event.x - joining_lines.x
        expected_y1 = pdf_event_area.y + pdf_event.top() - joining_lines.y
        expected_x2 = pdf_scale.right() - joining_lines.x
        expected_y2 = (
                pdf_scale.y
                + pdf_event.position_on_scale
                + pdf_event.height
                - joining_lines.y
        )
        self.assertEqual(line.x1, expected_x1)
        self.assertEqual(line.y1, expected_y1)
        self.assertEqual(line.x2, expected_x2)
        self.assertEqual(line.y2, expected_y2)
