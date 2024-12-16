
from reportlab.lib.units import mm

from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeTimeline
from timelines.models import EventArea
from timelines.pdf.layout import (
    DEFAULT_PAGE_BORDER,
    DEFAULT_COMPONENT_BORDER,
    A3_SHORT
)
from timelines.pdf.portrait_layout import PortraitLayout


TITLE_HEIGHT = 20 * mm
DESCRIPTION_HEIGHT = 40 * mm
TAG_KEY_HEIGHT = 30 * mm

SCALE_WIDTH = 40 * mm
SCALE_HEIGHT = 800 * mm
EVENT_AREA_0_WEIGHT = 5
EVENT_AREA_1_WEIGHT = 2
TOTAL_EVENT_AREA_WEIGHT = (
    EVENT_AREA_0_WEIGHT + EVENT_AREA_1_WEIGHT
)
EVENT_AND_SCALE_AREA_WIDTH = (
    A3_SHORT - (2 * DEFAULT_PAGE_BORDER)
)
COMBINED_EVENT_AREA_WIDTH = (
    EVENT_AND_SCALE_AREA_WIDTH
    - SCALE_WIDTH
    - (2 * DEFAULT_COMPONENT_BORDER)
)
EVENT_AREA_0_WIDTH = (
    COMBINED_EVENT_AREA_WIDTH
    * (EVENT_AREA_0_WEIGHT / TOTAL_EVENT_AREA_WEIGHT)
)
EVENT_AREA_1_WIDTH = (
    COMBINED_EVENT_AREA_WIDTH
    * (EVENT_AREA_1_WEIGHT / TOTAL_EVENT_AREA_WEIGHT)
)
PAGE_HEIGHT = (
    TITLE_HEIGHT
    + DESCRIPTION_HEIGHT
    + SCALE_HEIGHT
    + TAG_KEY_HEIGHT
    + (3 * DEFAULT_COMPONENT_BORDER)
    + (2 * DEFAULT_PAGE_BORDER)
)
HEIGHT_INCREASE = 55 * mm


class PDFTimelineLayoutPortraitTest(TestCase):
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
            scale_unit_length=5,
            page_size="3",
            page_orientation="P",
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
        self.layout = PortraitLayout(age_timeline)
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
        expected_width = A3_SHORT
        expected_height = PAGE_HEIGHT
        test_area = self.layout.page_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_drawable_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = A3_SHORT - (2 * DEFAULT_PAGE_BORDER)
        expected_height = PAGE_HEIGHT - (2 * DEFAULT_PAGE_BORDER)
        test_area = self.layout.drawable_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_title_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = PAGE_HEIGHT - DEFAULT_PAGE_BORDER - TITLE_HEIGHT
        expected_width = A3_SHORT - (2 * DEFAULT_PAGE_BORDER)
        expected_height = TITLE_HEIGHT
        test_area = self.layout.title_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_description_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            PAGE_HEIGHT
            - DEFAULT_PAGE_BORDER
            - TITLE_HEIGHT
            - DEFAULT_COMPONENT_BORDER
            - DESCRIPTION_HEIGHT
        )
        expected_width = A3_SHORT - (2 * DEFAULT_PAGE_BORDER)
        expected_height = DESCRIPTION_HEIGHT
        test_area = self.layout.description_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_tag_key_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = A3_SHORT - (2 * DEFAULT_PAGE_BORDER)
        expected_height = TAG_KEY_HEIGHT
        test_area = self.layout.tag_key_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_and_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + TAG_KEY_HEIGHT
            + DEFAULT_COMPONENT_BORDER
        )
        expected_width = EVENT_AND_SCALE_AREA_WIDTH
        expected_height = SCALE_HEIGHT
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
        expected_width = EVENT_AREA_0_WIDTH
        expected_height = SCALE_HEIGHT
        test_area = self.layout.event_areas[0]
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_scale_area(self):
        expected_x = (
            DEFAULT_PAGE_BORDER
            + EVENT_AREA_0_WIDTH
            + DEFAULT_COMPONENT_BORDER
        )
        expected_y = (
            DEFAULT_PAGE_BORDER
            + TAG_KEY_HEIGHT
            + DEFAULT_COMPONENT_BORDER
        )
        expected_width = SCALE_WIDTH
        expected_height = SCALE_HEIGHT
        test_area = self.layout.scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_area_1(self):
        expected_x = (
            DEFAULT_PAGE_BORDER
            + EVENT_AREA_0_WIDTH
            + SCALE_WIDTH
            + (2 * DEFAULT_COMPONENT_BORDER)
        )
        expected_y = (
            DEFAULT_PAGE_BORDER
            + TAG_KEY_HEIGHT
            + DEFAULT_COMPONENT_BORDER
        )
        expected_width = EVENT_AREA_1_WIDTH
        expected_height = SCALE_HEIGHT
        test_area = self.layout.event_areas[1]
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertAlmostEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_expand(self):
        self.layout.expand_event_overlap(HEIGHT_INCREASE)
        expected_page_height = (
            PAGE_HEIGHT + HEIGHT_INCREASE
        )
        self.assertEqual(
            self.layout.page_area.height,
            expected_page_height
        )
        expected_drawable_height = (
            PAGE_HEIGHT
            - (2 * DEFAULT_PAGE_BORDER)
            + HEIGHT_INCREASE
        )
        self.assertEqual(
            self.layout.drawable_area.height,
            expected_drawable_height
        )
        expected_title_y = (
            PAGE_HEIGHT + HEIGHT_INCREASE - DEFAULT_PAGE_BORDER - TITLE_HEIGHT
        )
        self.assertEqual(
            self.layout.title_area.y,
            expected_title_y
        )
        expected_description_y = (
            expected_title_y - DESCRIPTION_HEIGHT - DEFAULT_COMPONENT_BORDER
        )
        self.assertEqual(
            self.layout.description_area.y,
            expected_description_y
        )
        expected_tag_key_y = DEFAULT_PAGE_BORDER
        self.assertEqual(
            self.layout.tag_key_area.y,
            expected_tag_key_y
        )
        expected_event_and_scale_area_y = (
            expected_tag_key_y
            + TAG_KEY_HEIGHT
            + DEFAULT_COMPONENT_BORDER
            + HEIGHT_INCREASE
        )
        self.assertEqual(
            self.layout.event_and_scale_area.y,
            expected_event_and_scale_area_y
        )
        self.assertEqual(
            self.layout.event_areas[0].y,
            expected_event_and_scale_area_y
        )
        self.assertEqual(
            self.layout.scale_area.y,
            expected_event_and_scale_area_y
        )
        self.assertEqual(
            self.layout.event_areas[1].y,
            expected_event_and_scale_area_y
        )
