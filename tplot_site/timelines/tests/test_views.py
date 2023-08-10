from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from age_timelines.models import AgeTimeline


class UserTimelinesViewTest(TestCase):
    TIMELINE_COUNT = 3

    @classmethod
    def setUpTestData(self):
        test_user_1 = User.objects.create_user(
            username="TestUser1",
            password="TestUser1#"
        )
        for i in range(self.TIMELINE_COUNT):
            AgeTimeline.objects.create(
                user=test_user_1,
                title=f"{test_user_1.username} AgeTimeline {i}",
            )

        test_user_2 = User.objects.create_user(
            username="TestUser2",
            password="TestUser2#"
        )
        for i in range(self.TIMELINE_COUNT):
            AgeTimeline.objects.create(
                user=test_user_2,
                title=f"{test_user_2.username} AgeTimeline {i}",
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("timelines:user-timelines"))
        self.assertRedirects(response, "/accounts/login/?next=/timelines/")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="TestUser1", password="TestUser1#")
        response = self.client.get("/timelines/")
        self.assertEqual(str(response.context['user']), "TestUser1")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="TestUser1", password="TestUser1#")
        response = self.client.get(reverse("timelines:user-timelines"))
        self.assertEqual(str(response.context['user']), "TestUser1")
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username="TestUser1", password="TestUser1#")
        response = self.client.get(reverse("timelines:user-timelines"))
        self.assertEqual(str(response.context['user']), "TestUser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "timelines/user_timelines.html")

    def test_lists_age_timelines_owned_by_logged_in_user(self):
        self.client.login(username="TestUser1", password="TestUser1#")
        response = self.client.get(reverse("timelines:user-timelines"))
        self.assertEqual(str(response.context['user']), "TestUser1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue('age_timeline_list' in response.context)
        age_timeline_list = response.context['age_timeline_list']
        self.assertEqual(len(age_timeline_list), self.TIMELINE_COUNT)
        for age_timeline in age_timeline_list:
            self.assertEqual(
                age_timeline.get_owner(),
                response.context['user']
            )
