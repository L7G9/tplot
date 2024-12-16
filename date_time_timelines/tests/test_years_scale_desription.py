from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from date_time_timelines.models import (
    DateTimeEvent,
    DateTimeTimeline,
    YEAR_10,
)
from date_time_timelines.pdf.date_time import DateTime
from date_time_timelines.pdf.years_scale_description import (
    YearsScaleDescription,
)
from timelines.pdf.round import Round


class YearsScaleDescriptionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )

        date_time_timeline = DateTimeTimeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_unit=YEAR_10,
            scale_unit_length=10,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        DateTimeEvent.objects.create(
            date_time_timeline=date_time_timeline,
            timeline_id=date_time_timeline.timeline_ptr.pk,
            title="Title",
            start_date_time=datetime(year=2004, month=1, day=15),
            has_end=True,
            end_date_time=datetime(year=2032, month=6, day=23),
        )
        self.scale_description = YearsScaleDescription(
            date_time_timeline
        )

        date_time_timeline_no_events = DateTimeTimeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_unit=YEAR_10,
            scale_unit_length=10,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scale_description_no_events = (
            YearsScaleDescription(date_time_timeline_no_events)
        )

    def test_start_date_time(self):
        result = self.scale_description.start_date_time.date_time
        expected = datetime(year=2000, month=1, day=1)
        self.assertEqual(result, expected)

    def test_end_date_time(self):
        result = self.scale_description.end_date_time.date_time
        expected = datetime(year=2040, month=1, day=1)
        self.assertEqual(result, expected)

    def test_get_scale_units(self):
        result = self.scale_description.get_scale_units()
        self.assertEqual(result, 4)

    def test_get_scale_units_no_events(self):
        result = self.scale_description_no_events.get_scale_units()
        self.assertEqual(result, 1)

    def test_get_scale_unit_length(self):
        result = self.scale_description.get_scale_unit_length()
        self.assertEqual(result, 400)

    def test_get_scale_label(self):
        result = self.scale_description.get_scale_label(1)
        self.assertEqual(result, "2010-01-01 00:00:00")

    def test_plot_2000_01_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2000, month=1, day=1))
        )
        self.assertEqual(result, 0.0)

    def test_plot_2000_01_16_12_00_00(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2000, month=1, day=16, hour=12))
        )
        self.assertAlmostEqual(result, 5 / 12)

    def test_plot_2000_02_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2000, month=2, day=1))
        )
        self.assertAlmostEqual(result, 5 / 6)

    def test_plot_2001_01_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2001, month=1, day=1))
        )
        self.assertEqual(result, 10.0)

    def test_plot_2002_07_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2002, month=7, day=1))
        )
        self.assertEqual(result, 25.0)

    def test_plot_2005_01_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2005, month=1, day=1))
        )
        self.assertEqual(result, 50.0)

    def test_plot_2010_01_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2010, month=1, day=1))
        )
        self.assertEqual(result, 100.0)

    def test_round_datetime_years(self):
        in_datetime = datetime(
            year=2003, month=2, day=3, hour=4, minute=23, second=44
        )
        result = self.scale_description.round_datetime(
            in_datetime, YEAR_10, Round.DOWN
        )
        expected = datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)

    def test_get_remaining_scale_units_for_seconds(self):
        in_datetime = datetime(
            year=2000, month=4, day=16, hour=0, minute=0, second=0
        )
        result = self.scale_description.get_remaining_scale_units_for_seconds(
            in_datetime, 6
        )
        self.assertEqual(result, 1 / 12)

    def test_get_remaining_scale_units_for_months(self):
        in_datetime = datetime(
            year=2000, month=4, day=16, hour=0, minute=0, second=0
        )
        result = self.scale_description.get_remaining_scale_units_for_months(
            in_datetime, 6
        )
        self.assertEqual(result, 1 / 2)
