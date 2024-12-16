from django.contrib.auth.models import User
from django.test import TestCase

from historical_timelines.models import HistoricalEvent, HistoricalTimeline
from historical_timelines.historical_year import HistoricalYear
from historical_timelines.pdf.historical_scale_description import (
    HistoricalScaleDescription,
)


class HistoricalTimelineScaleDescriptionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )

        historical_timeline = HistoricalTimeline.objects.create(
            user=user,
            title="Test Historical Timeline Title",
            description="Test Historical Timeline Description",
            scale_unit=5,
            scale_unit_length=10,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        HistoricalEvent.objects.create(
            historical_timeline=historical_timeline,
            timeline_id=historical_timeline.timeline_ptr.pk,
            title="Title",
            start_bc_ad=1,
            start_year=6,
            has_end=False,
        )
        HistoricalEvent.objects.create(
            historical_timeline=historical_timeline,
            timeline_id=historical_timeline.timeline_ptr.pk,
            title="Title",
            start_bc_ad=1,
            start_year=7,
            has_end=True,
            end_bc_ad=1,
            end_year=22,
        )
        self.scale_description = HistoricalScaleDescription(
            historical_timeline
        )

        historical_timeline_no_events = HistoricalTimeline.objects.create(
            user=user,
            title="Test Historical Timeline Title",
            description="Test Historical Timeline Description",
            scale_unit=5,
            scale_unit_length=10,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scale_description_no_events = HistoricalScaleDescription(
            historical_timeline_no_events
        )

    def test_start_historical(self):
        years = self.scale_description.start.year
        self.assertEqual(years, 5)

    def test_end_historical(self):
        years = self.scale_description.end.year
        self.assertEqual(years, 25)

    def test_get_scale_units(self):
        scale_units = self.scale_description.get_scale_units()
        self.assertEqual(scale_units, 4)

    def test_get_scale_units_no_events(self):
        scale_units = self.scale_description_no_events.get_scale_units()
        self.assertEqual(scale_units, 1)

    def test_get_scale_unit_length(self):
        scale_unit_length = self.scale_description.get_scale_unit_length()
        self.assertEqual(scale_unit_length, 400)

    def test_get_scale_label(self):
        scale_label = self.scale_description.get_scale_label(0)
        self.assertEqual(scale_label, "5 AD")

    def test_plot_year_5AD(self):
        offset = self.scale_description.plot(HistoricalYear(5))
        self.assertEqual(offset, 0.0)

    def test_plot_year_10AD(self):
        offset = self.scale_description.plot(HistoricalYear(10))
        self.assertEqual(offset, 100.0)

    def test_plot_year_25AD(self):
        offset = self.scale_description.plot(HistoricalYear(25))
        self.assertEqual(offset, 400.0)
