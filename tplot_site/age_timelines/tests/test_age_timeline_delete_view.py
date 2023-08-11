from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from age_timelines.models import AgeTimeline

class AgeTimelineDetailViewTest(TestCase):
    USER_COUNT = 2
    TIMELINES_PER_USER = 1

    @classmethod
    def setUpTestData(cls):
        populate_db(
            cls.USER_COUNT,
            cls.TIMELINES_PER_USER,
            0,
            0,
            0
        )
        cls.user_0 = User.objects.get(username="test_user_0")
        cls.user_0_pw = "TestUser0#"
        cls.user_1 = User.objects.get(username="test_user_1")
        cls.age_timeline_0 = AgeTimeline.objects.get(user=cls.user_0)
        cls.age_timeline_1 = AgeTimeline.objects.get(user=cls.user_1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("age_timelines:age-timeline-delete", kwargs={'pk': self.age_timeline_0.id}))
        self.assertRedirects(response, f"/accounts/login/?next=/timelines/age/{self.age_timeline_0.id}/delete/")

    def test_forbidden_if_not_owned_by_logged_in_user(self):
        self.client.login(username=self.user_0.username, password=self.user_0_pw)
        response = self.client.get(reverse("age_timelines:age-timeline-delete", kwargs={'pk': self.age_timeline_1.id}))
        self.assertEqual(response.status_code, 403)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username=self.user_0.username, password=self.user_0_pw)
        response = self.client.get(f"/timelines/age/{self.age_timeline_0.id}/delete/")
        self.assertEqual(str(response.context['user']), self.user_0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username=self.user_0.username, password=self.user_0_pw)
        response = self.client.get(reverse("age_timelines:age-timeline-delete", kwargs={'pk': self.age_timeline_0.id}))
        self.assertEqual(str(response.context['user']), self.user_0.username)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username=self.user_0.username, password=self.user_0_pw)
        response = self.client.get(reverse("age_timelines:age-timeline-delete", kwargs={'pk': self.age_timeline_0.id}))
        self.assertEqual(str(response.context['user']), self.user_0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "age_timelines/age_timeline_confirm_delete.html")

    def test_context_object_owned_by_logged_in_user(self):
        self.client.login(username=self.user_0.username, password=self.user_0_pw)
        response = self.client.get(reverse("age_timelines:age-timeline-delete", kwargs={'pk': self.age_timeline_0.id}))
        self.assertTrue('object' in response.context)
        self.assertEqual(response.context['object'].get_owner(), response.context['user'])

    def test_age_timeline_deleted(self):
        self.client.login(username=self.user_0.username, password=self.user_0_pw)
        response = self.client.post(reverse('age_timelines:age-timeline-delete', kwargs={'pk': self.age_timeline_0.id}), follow=True)
        age_timelines = AgeTimeline.objects.filter(user=self.user_0)
        self.assertEqual(len(age_timelines), self.TIMELINES_PER_USER-1)

    def test_redirect_to_user_timelines_on_delete(self):
        self.client.login(username=self.user_0.username, password=self.user_0_pw)
        response = self.client.post(reverse('age_timelines:age-timeline-delete', kwargs={'pk': self.age_timeline_0.id}), follow=True)
        self.assertRedirects(response, reverse('timelines:user-timelines'), status_code=302)
