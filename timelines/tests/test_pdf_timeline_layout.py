from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeEvent, AgeTimeline
from age_timelines.pdf.age_timeline_scale_description import AgeTimelineScaleDescription
from timelines.models import EventArea
from timelines.pdf.timeline_layout import TimelineLayout

class TimelineLayoutTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )

        landscape_age_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=5,
            scale_length=5,
            page_size="4",
            page_orientation="L",
            page_scale_position=1,
        )
        EventArea.objects.create(
            timeline=landscape_age_timeline.timeline_ptr,
            name="Event Area 1",
            page_position=0,
            weight=1,
        )
        EventArea.objects.create(
            timeline=landscape_age_timeline.timeline_ptr,
            name="Event Area 2",
            page_position=2,
            weight=2,
        )
        AgeEvent.objects.create(
            age_timeline=landscape_age_timeline,
            timeline_id=landscape_age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=0,
            start_month=0,
            has_end=False,
        )
        AgeEvent.objects.create(
            age_timeline=landscape_age_timeline,
            timeline_id=landscape_age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=20,
            start_month=0,
            has_end=False,
        )
        self.landscape_layout = TimelineLayout(
            landscape_age_timeline,
            AgeTimelineScaleDescription(landscape_age_timeline),
            scale_size=10
        )
        self.landscape_layout.create_layout(20, 10)

    def test_landscape_page_area(self):
        area = self.landscape_layout.page_area
        self.assertEqual(area.x, 0)
        self.assertEqual(area.y, 0)
        self.assertEqual(area.width, 220)
        self.assertEqual(area.height, 210)

    def test_drawable_area(self):
        area = self.landscape_layout.drawable_area
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 10)
        self.assertEqual(area.width, 200)
        self.assertEqual(area.height, 190)

    def test_title_area(self):
        area = self.landscape_layout.title_area
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 180)
        self.assertEqual(area.width, 200)
        self.assertEqual(area.height, 20)

    def test_description_area(self):
        area = self.landscape_layout.description_area
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 170)
        self.assertEqual(area.width, 200)
        self.assertEqual(area.height, 10)

    def test_landscape_event_and_scale_area(self):
        area = self.landscape_layout.event_and_scale_area
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 10)
        self.assertEqual(area.width, 200)
        self.assertEqual(area.height, 160)

    def test_landscape_event_area_0(self):
        area = self.landscape_layout.event_areas[0]
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 10)
        self.assertEqual(area.width, 200)
        self.assertEqual(area.height, 50)

    def test_landscape_scale_area(self):
        area = self.landscape_layout.scale_area
        self.assertEqual(area.x, 0)
        self.assertEqual(area.y, 60)
        self.assertEqual(area.width, 220)
        self.assertEqual(area.height, 10)

    def test_landscape_event_area_1(self):
        area = self.landscape_layout.event_areas[1]
        self.assertEqual(area.x, 10)
        self.assertEqual(area.y, 70)
        self.assertEqual(area.width, 200)
        self.assertEqual(area.height, 100)
