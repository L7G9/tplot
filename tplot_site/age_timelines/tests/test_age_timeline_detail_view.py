from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db


class AgeTimelineDetailViewTest(TestCase):
    USER_COUNT = 2
    TIMELINE_COUNT = 1
    EVENT_COUNT = 6
    TAG_COUNT = 3
    AREA_COUNT = 2

    @classmethod
    def setUpTestData(self):
        populate_db(
            self.USER_COUNT,
            self.TIMELINE_COUNT,
            self.EVENT_COUNT,
            self.TAG_COUNT,
            self.AREA_COUNT
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("age_timelines:age-timeline-detail", kwargs={'pk': 1}))
        self.assertRedirects(response, "/accounts/login/?next=/timelines/age/1/detail/")

    def test_forbidden_if_not_owned_by_logged_in_user(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-detail", kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get("/timelines/age/1/detail/")
        self.assertEqual(str(response.context['user']), "test_user_0")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-detail", kwargs={'pk': 1}))
        self.assertEqual(str(response.context['user']), "test_user_0")
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-detail", kwargs={'pk': 1}))
        self.assertEqual(str(response.context['user']), "test_user_0")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "age_timelines/age_timeline_detail.html")

    def test_context_object_owned_by_logged_in_user(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-detail", kwargs={'pk': 1}))

        self.assertTrue('object' in response.context)
        self.assertEqual(response.context['object'].get_owner(), response.context['user'])

    def test_age_events_owned_by_logged_in_user(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-detail", kwargs={'pk': 1}))

        age_events = response.context['object'].ageevent_set.all()
        self.assertEqual(len(age_events), self.EVENT_COUNT)
        for age_Event in age_events:
            self.assertEqual(age_Event.get_owner(), response.context['user'])

    def test_tags_owned_by_logged_in_user(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-detail", kwargs={'pk': 1}))

        tags = response.context['object'].tag_set.all()
        self.assertEqual(len(tags), self.TAG_COUNT)
        for tag in tags:
            self.assertEqual(tag.get_owner(), response.context['user'])

    def test_event_areas_owned_by_logged_in_user(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-detail", kwargs={'pk': 1}))

        areas = response.context['object'].eventarea_set.all()
        self.assertEqual(len(areas), self.AREA_COUNT)
        for area in areas:
            self.assertEqual(area.get_owner(), response.context['user'])
