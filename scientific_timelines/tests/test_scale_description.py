from django.contrib.auth.models import User
from django.test import TestCase

from scientific_timelines.models import ScientificEvent, ScientificTimeline
from scientific_timelines.scientific_year import ScientificYear
from scientific_timelines.pdf.scientific_scale_description import (
    ScientificScaleDescription,
)


class ScientificTimelineScaleDescriptionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )

        scientific_timeline = ScientificTimeline.objects.create(
            user=user,
            title="Test Scientific Timeline Title",
            description="Test Scientific Timeline Description",
            scale_unit=1000,
            scale_unit_length=10,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        ScientificEvent.objects.create(
            scientific_timeline=scientific_timeline,
            timeline_id=scientific_timeline.timeline_ptr.pk,
            title="Title",
            start_year_fraction=-0.5,
            start_multiplier=1000,
            has_end=False,
        )
        ScientificEvent.objects.create(
            scientific_timeline=scientific_timeline,
            timeline_id=scientific_timeline.timeline_ptr.pk,
            title="Title",
            start_year_fraction=2,
            start_multiplier=1000,
            has_end=True,
            end_year_fraction=4.5,
            end_multiplier=1000,
        )
        self.scale_description = ScientificScaleDescription(
            scientific_timeline
        )

        scientific_timeline_no_events = ScientificTimeline.objects.create(
            user=user,
            title="Test Scientific Timeline Title",
            description="Test Scientific Timeline Description",
            scale_unit=1000,
            scale_unit_length=10,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scale_description_no_events = ScientificScaleDescription(
            scientific_timeline_no_events
        )

    def test_start_scientific(self):
        start = self.scale_description.start
        self.assertEqual(start.fraction, -1.0)
        self.assertEqual(start.multiplier, 1000)

    def test_end_scientific(self):
        end = self.scale_description.end
        self.assertEqual(end.fraction, 5)
        self.assertEqual(end.multiplier, 1000)

    def test_get_scale_units(self):
        scale_units = self.scale_description.get_scale_units()
        self.assertEqual(scale_units, 6)

    def test_get_scale_units_no_events(self):
        scale_units = self.scale_description_no_events.get_scale_units()
        self.assertEqual(scale_units, 1)

    def test_get_scale_unit_length(self):
        scale_unit_length = self.scale_description.get_scale_unit_length()
        self.assertEqual(scale_unit_length, 600)

    def test_get_scale_label(self):
        scale_label = self.scale_description.get_scale_label(0)
        self.assertEqual(scale_label, "1.0 thousand years ago")

    def test_plot_start(self):
        offset = self.scale_description.plot(ScientificYear(-1.0, 1000))
        self.assertEqual(offset, 0.0)

    def test_plot_middle(self):
        offset = self.scale_description.plot(ScientificYear(1.5, 1000))
        self.assertEqual(offset, 250.0)

    def test_plot_end(self):
        offset = self.scale_description.plot(ScientificYear(5.0, 1000))
        self.assertEqual(offset, 600.0)
