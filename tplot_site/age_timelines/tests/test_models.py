from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeEvent, AgeTimeline


class AgeTimelineModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser",
            password="TestUser01#"
        )
        age_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=10,
            scale_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.age_timeline_id = age_timeline.id

    def test_scale_unit_choices(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        choices = age_timeline._meta.get_field('scale_unit').choices
        self.assertEqual(choices, AgeTimeline.SCALE_UNITS)

    def test_scalue_unit_default(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        default = age_timeline._meta.get_field('scale_unit').default
        self.assertEqual(default, 10)

    def test_ordering_by_title(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        ordering = age_timeline._meta.ordering
        self.assertEqual(len(ordering), 1)
        self.assertEqual(ordering[0], "title")

    def test_object_name_is_title(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        title = age_timeline.title
        self.assertEqual(str(age_timeline), title)

    def test_(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        owner = age_timeline.user
        self.assertEqual(age_timeline.get_owner(), owner)
