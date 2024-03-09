from reportlab.lib.units import mm

from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeTimeline
from timelines.models import EventArea
from timelines.pdf.pdf_timeline_layout import (
    PDFTimelineLayout,
    DEFAULT_PAGE_BORDER,
    DEFAULT_COMPONENT_BORDER,
    A4_SHORT,
    A3_SHORT
)


TITLE_HEIGHT = 20 * mm
DESCRIPTION_HEIGHT = 40 * mm

LANDSCAPE_SCALE_WIDTH = 300 * mm
LANDSCAPE_SCALE_HEIGHT = 20 * mm
LANDSCAPE_EVENT_AREA_0_WEIGHT = 1
LANDSCAPE_EVENT_AREA_1_WEIGHT = 2
LANDSCAPE_TOTAL_EVENT_AREA_WEIGHT = (
    LANDSCAPE_EVENT_AREA_0_WEIGHT + LANDSCAPE_EVENT_AREA_1_WEIGHT
)
LANDSCAPE_EVENT_AND_SCALE_AREA_HEIGHT = (
    A4_SHORT
    - (2 * DEFAULT_PAGE_BORDER)
    - TITLE_HEIGHT
    - DESCRIPTION_HEIGHT
    - (2 * DEFAULT_COMPONENT_BORDER)
)

LANDSCAPE_COMBINED_EVENT_AREA_HEIGHT = (
    LANDSCAPE_EVENT_AND_SCALE_AREA_HEIGHT
    - LANDSCAPE_SCALE_HEIGHT
    - (2 * DEFAULT_COMPONENT_BORDER)
)

LANDSCAPE_EVENT_AREA_0_HEIGHT = (
    LANDSCAPE_COMBINED_EVENT_AREA_HEIGHT
    * (LANDSCAPE_EVENT_AREA_0_WEIGHT / LANDSCAPE_TOTAL_EVENT_AREA_WEIGHT)
)
LANDSCAPE_EVENT_AREA_1_HEIGHT = (
    LANDSCAPE_COMBINED_EVENT_AREA_HEIGHT
    * (LANDSCAPE_EVENT_AREA_1_WEIGHT / LANDSCAPE_TOTAL_EVENT_AREA_WEIGHT)
)
LANDSCAPE_WIDTH_INCREASE = 40 * mm


class PDFTimelineLayoutLandscapeTest(TestCase):
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
            weight=LANDSCAPE_EVENT_AREA_0_WEIGHT,
        )
        EventArea.objects.create(
            timeline=age_timeline.timeline_ptr,
            name="Event Area 1",
            page_position=2,
            weight=LANDSCAPE_EVENT_AREA_1_WEIGHT,
        )
        self.layout = PDFTimelineLayout(age_timeline)
        self.layout.set_dimensions(
            TITLE_HEIGHT,
            DESCRIPTION_HEIGHT,
            LANDSCAPE_SCALE_WIDTH,
            LANDSCAPE_SCALE_HEIGHT
        )

    def test_page_area(self):
        expected_x = 0.0
        expected_y = 0.0
        expected_width = LANDSCAPE_SCALE_WIDTH + (2 * DEFAULT_PAGE_BORDER)
        expected_height = A4_SHORT
        test_area = self.layout.page_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_drawable_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = A4_SHORT - (2 * DEFAULT_PAGE_BORDER)
        test_area = self.layout.drawable_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_title_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = A4_SHORT - DEFAULT_PAGE_BORDER - TITLE_HEIGHT
        expected_width = LANDSCAPE_SCALE_WIDTH
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
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = DESCRIPTION_HEIGHT
        test_area = self.layout.description_area
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_and_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = LANDSCAPE_EVENT_AND_SCALE_AREA_HEIGHT
        test_area = self.layout.event_and_scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_area_0(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = LANDSCAPE_EVENT_AREA_0_HEIGHT
        test_area = self.layout.event_areas[0]
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + LANDSCAPE_EVENT_AREA_0_HEIGHT
            + DEFAULT_COMPONENT_BORDER
        )
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = LANDSCAPE_SCALE_HEIGHT
        test_area = self.layout.scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_area_1(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + LANDSCAPE_EVENT_AREA_0_HEIGHT
            + LANDSCAPE_SCALE_HEIGHT
            + (2 * DEFAULT_COMPONENT_BORDER)
        )
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = LANDSCAPE_EVENT_AREA_1_HEIGHT
        test_area = self.layout.event_areas[1]
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_expand(self):
        self.layout.expand_event_overlap(LANDSCAPE_WIDTH_INCREASE)
        expected_page_width = (
            LANDSCAPE_SCALE_WIDTH
            + (2 * DEFAULT_PAGE_BORDER)
            + LANDSCAPE_WIDTH_INCREASE
        )
        expected_drawable_width = (
            LANDSCAPE_SCALE_WIDTH + LANDSCAPE_WIDTH_INCREASE
        )
        self.assertEqual(
            self.layout.page_area.width,
            expected_page_width
        )
        self.assertEqual(
            self.layout.drawable_area.width,
            expected_drawable_width
        )


PORTRAIT_SCALE_WIDTH = 40 * mm
PORTRAIT_SCALE_HEIGHT = 800 * mm
PORTRAIT_EVENT_AREA_0_WEIGHT = 5
PORTRAIT_EVENT_AREA_1_WEIGHT = 2
PORTRAIT_TOTAL_EVENT_AREA_WEIGHT = (
    PORTRAIT_EVENT_AREA_0_WEIGHT + PORTRAIT_EVENT_AREA_1_WEIGHT
)
PORTRAIT_EVENT_AND_SCALE_AREA_WIDTH = (
    A3_SHORT - (2 * DEFAULT_PAGE_BORDER)
)
PORTRAIT_COMBINED_EVENT_AREA_WIDTH = (
    PORTRAIT_EVENT_AND_SCALE_AREA_WIDTH
    - PORTRAIT_SCALE_WIDTH
    - (2 * DEFAULT_COMPONENT_BORDER)
)
PORTRAIT_EVENT_AREA_0_WIDTH = (
    PORTRAIT_COMBINED_EVENT_AREA_WIDTH
    * (PORTRAIT_EVENT_AREA_0_WEIGHT / PORTRAIT_TOTAL_EVENT_AREA_WEIGHT)
)
PORTRAIT_EVENT_AREA_1_WIDTH = (
    PORTRAIT_COMBINED_EVENT_AREA_WIDTH
    * (PORTRAIT_EVENT_AREA_1_WEIGHT / PORTRAIT_TOTAL_EVENT_AREA_WEIGHT)
)
PORTRAIT_PAGE_HEIGHT = (
    TITLE_HEIGHT
    + DESCRIPTION_HEIGHT
    + PORTRAIT_SCALE_HEIGHT
    + (2 * DEFAULT_COMPONENT_BORDER)
    + (2 * DEFAULT_PAGE_BORDER)
)
PORTRAIT_HEIGHT_INCREASE = 55 * mm


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
            scale_length=5,
            page_size="3",
            page_orientation="P",
            page_scale_position=1,
        )
        EventArea.objects.create(
            timeline=age_timeline.timeline_ptr,
            name="Event Area 0",
            page_position=0,
            weight=PORTRAIT_EVENT_AREA_0_WEIGHT,
        )
        EventArea.objects.create(
            timeline=age_timeline.timeline_ptr,
            name="Event Area 1",
            page_position=2,
            weight=PORTRAIT_EVENT_AREA_1_WEIGHT,
        )
        self.layout = PDFTimelineLayout(age_timeline)
        self.layout.set_dimensions(
            TITLE_HEIGHT,
            DESCRIPTION_HEIGHT,
            PORTRAIT_SCALE_WIDTH,
            PORTRAIT_SCALE_HEIGHT
        )

    def test_page_area(self):
        expected_x = 0.0
        expected_y = 0.0
        expected_width = A3_SHORT
        expected_height = PORTRAIT_PAGE_HEIGHT
        test_area = self.layout.page_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_drawable_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = A3_SHORT - (2 * DEFAULT_PAGE_BORDER)
        expected_height = PORTRAIT_PAGE_HEIGHT - (2 * DEFAULT_PAGE_BORDER)
        test_area = self.layout.drawable_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_title_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = PORTRAIT_PAGE_HEIGHT - DEFAULT_PAGE_BORDER - TITLE_HEIGHT
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
            PORTRAIT_PAGE_HEIGHT
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

    def test_event_and_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = PORTRAIT_EVENT_AND_SCALE_AREA_WIDTH
        expected_height = PORTRAIT_SCALE_HEIGHT
        test_area = self.layout.event_and_scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_area_0(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = PORTRAIT_EVENT_AREA_0_WIDTH
        expected_height = PORTRAIT_SCALE_HEIGHT
        test_area = self.layout.event_areas[0]
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_scale_area(self):
        expected_x = (
            DEFAULT_PAGE_BORDER
            + PORTRAIT_EVENT_AREA_0_WIDTH
            + DEFAULT_COMPONENT_BORDER
        )
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = PORTRAIT_SCALE_WIDTH
        expected_height = PORTRAIT_SCALE_HEIGHT
        test_area = self.layout.scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_event_area_1(self):
        expected_x = (
            DEFAULT_PAGE_BORDER
            + PORTRAIT_EVENT_AREA_0_WIDTH
            + PORTRAIT_SCALE_WIDTH
            + (2 * DEFAULT_COMPONENT_BORDER)
        )
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = PORTRAIT_EVENT_AREA_1_WIDTH
        expected_height = PORTRAIT_SCALE_HEIGHT
        test_area = self.layout.event_areas[1]
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertAlmostEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_expand(self):
        self.layout.expand_event_overlap(PORTRAIT_HEIGHT_INCREASE)
        expected_page_height = (
            PORTRAIT_PAGE_HEIGHT + PORTRAIT_HEIGHT_INCREASE
        )
        expected_drawable_height = (
            PORTRAIT_PAGE_HEIGHT
            - (2 * DEFAULT_PAGE_BORDER)
            + PORTRAIT_HEIGHT_INCREASE
        )
        self.assertEqual(
            self.layout.page_area.height,
            expected_page_height
        )
        self.assertEqual(
            self.layout.drawable_area.height,
            expected_drawable_height
        )
