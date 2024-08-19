from reportlab.lib.units import mm

from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeTimeline
from timelines.models import EventArea
from timelines.pdf.layout import (
    DEFAULT_PAGE_BORDER,
    DEFAULT_COMPONENT_BORDER,
    A4_SHORT,
)
from timelines.pdf.landscape_layout import LandscapeLayout


TITLE_HEIGHT = 20 * mm
DESCRIPTION_HEIGHT = 40 * mm
TAG_KEY_HEIGHT = 30 * mm

SCALE_WIDTH = 300 * mm
SCALE_HEIGHT = 20 * mm
EVENT_AREA_0_WEIGHT = 1
EVENT_AREA_1_WEIGHT = 2
TOTAL_EVENT_AREA_WEIGHT = (
    EVENT_AREA_0_WEIGHT + EVENT_AREA_1_WEIGHT
)
EVENT_AND_SCALE_AREA_HEIGHT = (
    A4_SHORT
    - (2 * DEFAULT_PAGE_BORDER)
    - TITLE_HEIGHT
    - DESCRIPTION_HEIGHT
    - TAG_KEY_HEIGHT
    - (3 * DEFAULT_COMPONENT_BORDER)
)

COMBINED_EVENT_AREA_HEIGHT = (
    EVENT_AND_SCALE_AREA_HEIGHT
    - SCALE_HEIGHT
    - (2 * DEFAULT_COMPONENT_BORDER)
)

EVENT_AREA_0_HEIGHT = (
    COMBINED_EVENT_AREA_HEIGHT
    * (EVENT_AREA_0_WEIGHT / TOTAL_EVENT_AREA_WEIGHT)
)
EVENT_AREA_1_HEIGHT = (
    COMBINED_EVENT_AREA_HEIGHT
    * (EVENT_AREA_1_WEIGHT / TOTAL_EVENT_AREA_WEIGHT)
)
WIDTH_INCREASE = 40 * mm


class LandscapeLayoutTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        age_timeline = AgeTimeline.objects.create(
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
            timeline=age_timeline.timeline_ptr,
            name="Event Area 0",
            page_position=0,
            weight=EVENT_AREA_0_WEIGHT,
        )
        EventArea.objects.create(
            timeline=age_timeline.timeline_ptr,
            name="Event Area 1",
            page_position=2,
            weight=EVENT_AREA_1_WEIGHT,
        )
        self.layout = LandscapeLayout(age_timeline)
        self.layout.set_dimensions(
            TITLE_HEIGHT,
            DESCRIPTION_HEIGHT,
            SCALE_WIDTH,
            SCALE_HEIGHT,
            TAG_KEY_HEIGHT,
        )

    def test_page_area(self):
        expected_x = 0.0
        expected_y = 0.0
        expected_width = SCALE_WIDTH + (2 * DEFAULT_PAGE_BORDER)
        expected_height = A4_SHORT
        test_area = self.layout.page_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_drawable_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = SCALE_WIDTH
        expected_height = A4_SHORT - (2 * DEFAULT_PAGE_BORDER)
        test_area = self.layout.drawable_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_title_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = A4_SHORT - DEFAULT_PAGE_BORDER - TITLE_HEIGHT
        expected_width = SCALE_WIDTH
        expected_height = TITLE_HEIGHT
        test_area = self.layout.title_area
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_description_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            A4_SHORT
            - DEFAULT_PAGE_BORDER
            - TITLE_HEIGHT
            - DEFAULT_COMPONENT_BORDER
            - DESCRIPTION_HEIGHT
        )
        expected_width = SCALE_WIDTH
        expected_height = DESCRIPTION_HEIGHT
        test_area = self.layout.description_area
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_tag_key_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = SCALE_WIDTH
        expected_height = TAG_KEY_HEIGHT
        test_area = self.layout.tag_key_area
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_and_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + TAG_KEY_HEIGHT
            + DEFAULT_COMPONENT_BORDER
        )
        expected_width = SCALE_WIDTH
        expected_height = EVENT_AND_SCALE_AREA_HEIGHT
        test_area = self.layout.event_and_scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_area_0(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + TAG_KEY_HEIGHT
            + DEFAULT_COMPONENT_BORDER
        )
        expected_width = SCALE_WIDTH
        expected_height = EVENT_AREA_0_HEIGHT
        test_area = self.layout.event_areas[0]
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + TAG_KEY_HEIGHT
            + EVENT_AREA_0_HEIGHT
            + (2 * DEFAULT_COMPONENT_BORDER)
        )
        expected_width = SCALE_WIDTH
        expected_height = SCALE_HEIGHT
        test_area = self.layout.scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_area_1(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + TAG_KEY_HEIGHT
            + EVENT_AREA_0_HEIGHT
            + SCALE_HEIGHT
            + (3 * DEFAULT_COMPONENT_BORDER)
        )
        expected_width = SCALE_WIDTH
        expected_height = EVENT_AREA_1_HEIGHT
        test_area = self.layout.event_areas[1]
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_expand(self):
        self.layout.expand_event_overlap(WIDTH_INCREASE)
        expected_page_width = (
            SCALE_WIDTH
            + (2 * DEFAULT_PAGE_BORDER)
            + WIDTH_INCREASE
        )
        expected_drawable_width = (
            SCALE_WIDTH + WIDTH_INCREASE
        )
        self.assertEqual(
            self.layout.page_area.width,
            expected_page_width
        )
        self.assertEqual(
            self.layout.drawable_area.width,
            expected_drawable_width
        )
