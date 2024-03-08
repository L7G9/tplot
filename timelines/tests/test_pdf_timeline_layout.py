from reportlab.lib.units import mm

from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeTimeline
from timelines.models import EventArea
from timelines.pdf.pdf_timeline_layout import (
    PDFTimelineLayout, DEFAULT_PAGE_BORDER, DEFAULT_COMPONENT_BORDER, A4_SHORT
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
            name="Event Area 0",
            page_position=0,
            weight=LANDSCAPE_EVENT_AREA_0_WEIGHT,
        )
        EventArea.objects.create(
            timeline=landscape_age_timeline.timeline_ptr,
            name="Event Area 1",
            page_position=2,
            weight=LANDSCAPE_EVENT_AREA_1_WEIGHT,
        )
        self.landscape_layout = PDFTimelineLayout(landscape_age_timeline)
        self.landscape_layout.set_dimensions(
            TITLE_HEIGHT,
            DESCRIPTION_HEIGHT,
            LANDSCAPE_SCALE_WIDTH,
            LANDSCAPE_SCALE_HEIGHT
        )

    def test_landscape_page_area(self):
        expected_x = 0.0
        expected_y = 0.0
        expected_width = LANDSCAPE_SCALE_WIDTH + (2 * DEFAULT_PAGE_BORDER)
        expected_height = A4_SHORT
        test_area = self.landscape_layout.page_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_landscape_drawable_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = A4_SHORT - (2 * DEFAULT_PAGE_BORDER)
        test_area = self.landscape_layout.drawable_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_landscape_title_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = A4_SHORT - DEFAULT_PAGE_BORDER - TITLE_HEIGHT
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = TITLE_HEIGHT
        test_area = self.landscape_layout.title_area
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_landscape_description_area(self):
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
        test_area = self.landscape_layout.description_area
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_landscape_event_and_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = LANDSCAPE_EVENT_AND_SCALE_AREA_HEIGHT
        test_area = self.landscape_layout.event_and_scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_landscape_event_area_0(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = LANDSCAPE_EVENT_AREA_0_HEIGHT
        test_area = self.landscape_layout.event_areas[0]
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_landscape_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + LANDSCAPE_EVENT_AREA_0_HEIGHT
            + DEFAULT_COMPONENT_BORDER
        )
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = LANDSCAPE_SCALE_HEIGHT
        test_area = self.landscape_layout.scale_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_landscape_event_area_1(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = (
            DEFAULT_PAGE_BORDER
            + LANDSCAPE_EVENT_AREA_0_HEIGHT
            + LANDSCAPE_SCALE_HEIGHT
            + (2 * DEFAULT_COMPONENT_BORDER)
        )
        expected_width = LANDSCAPE_SCALE_WIDTH
        expected_height = LANDSCAPE_EVENT_AREA_1_HEIGHT
        test_area = self.landscape_layout.event_areas[1]
        self.assertEqual(test_area.x, expected_x)
        self.assertAlmostEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_landscape_expand(self):
        self.landscape_layout.expand_event_overlap(LANDSCAPE_WIDTH_INCREASE)
        expected_page_width = (
            LANDSCAPE_SCALE_WIDTH
            + (2 * DEFAULT_PAGE_BORDER)
            + LANDSCAPE_WIDTH_INCREASE
        )
        expected_drawable_width = (
            LANDSCAPE_SCALE_WIDTH + LANDSCAPE_WIDTH_INCREASE
        )
        self.assertEqual(
            self.landscape_layout.page_area.width,
            expected_page_width
        )
        self.assertEqual(
            self.landscape_layout.drawable_area.width,
            expected_drawable_width
        )

"""
PORTRAIT_SCALE_WIDTH = 300 * mm
PORTRAIT_SCAlE_HEIGHT = 20 * mm
PORTRAIT_EVENT_AREA_0_WEIGHT = 1
PORTRAIT_EVENT_AREA_1_WEIGHT = 2
PORTRAIT_TOTAL_EVENT_AREA_WEIGHT = PORTRAIT_EVENT_AREA_0_WEIGHT + PORTRAIT_EVENT_AREA_1_WEIGHT
PORTRAIT_EVENT_AND_SCALE_AREA_WIDTH = A4_SHORT - (2 * DEFAULT_PAGE_BORDER)
PORTRAIT_EVENT_AREA_0_WIDTH = (PORTRAIT_EVENT_AND_SCALE_AREA_WIDTH - PORTRAIT_SCAlE_HEIGHT) * (PORTRAIT_EVENT_AREA_0_WEIGHT / PORTRAIT_TOTAL_EVENT_AREA_WEIGTH)
PORTRAIT_EVENT_AREA_1_WIDTH = (PORTRAIT_EVENT_AND_SCALE_AREA_WIDTH - PORTRAIT_SCAlE_HEIGHT) * (PORTRAIT_EVENT_AREA_1_WEIGHT / PORTRAIT_TOTAL_EVENT_AREA_WEIGTH)

class PDFTimelineLayoutPortraitTest(TestCase):
    @classmethod
    def setUpTestData(self):
        portrait_age_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=5,
            scale_length=5,
            page_size="4",
            page_orientation="P",
            page_scale_position=1,
        )

        EventArea.objects.create(
            timeline=portrait_age_timeline.timeline_ptr,
            name="Event Area 0",
            page_position=0,
            weight=EVENT_AREA_0_WEIGHT,
        )

        EventArea.objects.create(
            timeline=portrait_age_timeline.timeline_ptr,
            name="Event Area 1",
            page_position=2,
            weight=EVENT_AREA_1_WEIGHT,
        )

        self.portrait_layout = PDFTimelineLayout(portrait_age_timeline)
        self.portrait_layout.set_dimensions(
            TITLE_HEIGHT,
            DESCRIPTION_HEIGHT,
            LANDSCAPE_SCALE_WIDTH,
            LANDSCAPE_SCAlE_HEIGHT
        )

    def test_portrait_page_area(self):
        expected_x = 0.0
        expected_y = 0.0
        expected_width = A4_SHORT
        expected_height = TITLE_HEIGHT + DESCRIPTION_HEIGHT + SCAlE_HEIGHT + (2 * DEFAULT_PAGE_BORDER)
        test_area = self.landscape_layout.page_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_portrait_drawable_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = A4_SHORT - (2 * DEFAULT_PAGE_BORDER)
        expected_height = TITLE_HEIGHT + DESCRIPTION_HEIGHT + SCAlE_HEIGHT
        test_area = self.landscape_layout.drawable_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_portrait_title_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER + SCAlE_HEIGHT + DESCRIPTION_HEIGHT
        expected_width = A4_SHORT - (2 * DEFAULT_PAGE_BORDER)
        expected_height = TITLE_HEIGHT
        test_area = self.landscape_layout.title_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_portrait_description_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER + SCAlE_HEIGHT
        expected_width = A4_SHORT - (2 * DEFAULT_PAGE_BORDER)
        expected_height = DESCRIPTION_HEIGHT
        test_area = self.landscape_layout.description_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_portrait_event_and_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = SCALE_WIDTH
        expected_height = EVENT_AND_SCALE_AREA_HEIGHT
        test_area = self.landscape_layout.???_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_portrait_event_area_0(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER
        expected_width = SCALE_WIDTH
        expected_height = EVENT_AREA_0_HEIGHT
        test_area = self.landscape_layout.???_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_portrait_scale_area(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER + EVENT_AREA_0_HEIGHT
        expected_width = SCALE_WIDTH
        expected_height = SCAlE_HEIGHT
        test_area = self.landscape_layout.???_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_portrait_event_area_1(self):
        expected_x = DEFAULT_PAGE_BORDER
        expected_y = DEFAULT_PAGE_BORDER + EVENT_AREA_0_HEIGHT + SCAlE_HEIGHT
        expected_width = SCALE_WIDTH
        expected_height = EVENT_AREA_1_HEIGHT
        test_area = self.landscape_layout.???_area
        self.assertEqual(test_area.x, expected_x)
        self.assertEqual(test_area.y, expected_y)
        self.assertEqual(test_area.width, expected_width)
        self.assertEqual(test_area.height, expected_height)

    def test_portrait_expand(self):
        pass
"""
