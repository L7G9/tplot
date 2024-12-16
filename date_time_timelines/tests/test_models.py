from django.contrib.auth.models import User
from django.test import TestCase

from date_time_timelines.models import DateTimeTimeline

from date_time_timelines.models import (
    WEEK_1,
    MONTH_3,
    YEAR_100,
)


class DateTimeTimelineTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        self.timeline_weeks = DateTimeTimeline.objects.create(
            user=user,
            title="Test Date & Time Timeline Title",
            description="Test Date & Time Timeline Description",
            scale_unit=WEEK_1,
            scale_unit_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )

        self.timeline_months = DateTimeTimeline.objects.create(
            user=user,
            title="Test Date & Time Timeline Title",
            description="Test Date & Time Timeline Description",
            scale_unit=MONTH_3,
            scale_unit_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )

        self.timeline_years = DateTimeTimeline.objects.create(
            user=user,
            title="Test Date & Time Timeline Title",
            description="Test Date & Time Timeline Description",
            scale_unit=YEAR_100,
            scale_unit_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )

    def test_is_week_scale_unit_true(self):
        self.assertTrue(self.timeline_weeks.is_week_scale_unit())

    def test_is_week_scale_unit_false(self):
        self.assertFalse(self.timeline_months.is_week_scale_unit())

    def test_is_month_scale_unit_true(self):
        self.assertTrue(self.timeline_months.is_month_scale_unit())

    def test_is_month_scale_unit_false(self):
        self.assertFalse(self.timeline_weeks.is_month_scale_unit())

    def test_get_months_in_scale_unit(self):
        self.assertEqual(self.timeline_months.get_months_in_scale_unit(), 3)

    def test_is_year_scale_unit_true(self):
        self.assertTrue(self.timeline_years.is_year_scale_unit())

    def test_is_year_scale_unit_false(self):
        self.assertFalse(self.timeline_months.is_year_scale_unit())

    def test_get_years_in_scale_unit(self):
        self.assertEqual(
            self.timeline_years.get_years_in_scale_unit(),
            100
        )
