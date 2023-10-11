from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeEvent, AgeTimeline
from age_timelines.layout import AgeTimelineLayout


class AgeTimelineLayoutTest(TestCase):
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
            scale_length=4,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        AgeEvent.objects.create(
            age_timeline=age_timeline,
            timeline_id=age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=6,
            start_month=6,
            has_end=False,
        )

        self.age_event = AgeEvent.objects.create(
            age_timeline=age_timeline,
            timeline_id=age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=20,
            start_month=0,
            has_end=True,
            end_year=22,
            end_month=0,
        )

        AgeEvent.objects.create(
            age_timeline=age_timeline,
            timeline_id=age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=21,
            start_month=6,
            has_end=False,
        )

        self.layout: AgeTimelineLayout = AgeTimelineLayout(age_timeline)

    def test_total_months(self):
        months = self.layout.total_months(21, 6)
        self.assertEqual(months, 258)

    def test_start_months(self):
        months = self.layout.start_months(self.age_event)
        self.assertEqual(months, 240)

    def test_end_months(self):
        months = self.layout.end_months(self.age_event)
        self.assertEqual(months, 264)

    def test_get_smallest_age(self):
        age: int = self.layout.get_smallest_age()
        self.assertEqual(age, 78)

    def test_get_largest_age(self):
        age: int = self.layout.get_largest_age()
        self.assertEqual(age, 264)

    def test_get_start_year_positive(self):
        year: int = self.layout.get_start_year(78)
        self.assertEqual(year, 6)

    def test_round_year_down_positive(self):
        year: int = self.layout.round_year_down(6)
        self.assertEqual(year, 5)

    def test_get_start_year_negative(self):
        year: int = self.layout.get_start_year(-17)
        self.assertEqual(year, -2)

    def test_round_year_down_negative(self):
        year: int = self.layout.round_year_down(-2)
        self.assertEqual(year, -5)

    def test_get_end_year_positive(self):
        year: int = self.layout.get_end_year(264)
        self.assertEqual(year, 22)

    def test_round_year_up_positive(self):
        year: int = self.layout.round_year_up(22)
        self.assertEqual(year, 25)

    def test_get_end_year_negative(self):
        year: int = self.layout.get_end_year(-17)
        self.assertEqual(year, -1)

    def test_round_year_up_negative(self):
        year: int = self.layout.round_year_up(-1)
        self.assertEqual(year, 0)

    def test_get_scale_units(self):
        scale_units: int = self.layout.get_scale_units(5, 25)
        self.assertEqual(scale_units, 4)

    def test_get_scale_units_equal(self):
        scale_units: int = self.layout.get_scale_units(5, 5)
        self.assertEqual(scale_units, 1)

    def test_get_scale_length(self):
        scale_length: int = self.layout.get_scale_length(4)
        self.assertEqual(scale_length, 160)

    def test_get_axis_labels_all_positive(self):
        axis_labels: [float] = self.layout.get_axis_labels(5, 4)
        self.assertEqual(axis_labels, ["5", "10", "15", "20", "25"])

    def test_get_axis_labels_all_negative(self):
        axis_labels: [float] = self.layout.get_axis_labels(-30, 3)
        self.assertEqual(axis_labels, ["-30", "-25", "-20", "-15"])

    def test_get_axis_labels_all_positive_to_negative(self):
        axis_labels: [float] = self.layout.get_axis_labels(-10, 4)
        self.assertEqual(axis_labels, ["-10", "-5", "0", "5", "10"])

    def test_plot_start(self):
        distance: float = self.layout.plot(5, 0)
        self.assertAlmostEqual(distance, 0.0)

    def test_plot_between_scale_units(self):
        distance: float = self.layout.plot(7, 6)
        self.assertAlmostEqual(distance, 20.0)

    def test_plot_end(self):
        distance: float = self.layout.plot(25, 0)
        self.assertAlmostEqual(distance, 160.0)
