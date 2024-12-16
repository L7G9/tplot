from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from historical_timelines.models import HistoricalTimeline


class HistoricalTimelineCreateViewTest(TestCase):
    USER_COUNT = 1
    TIMELINES_PER_USER = 0

    @classmethod
    def setUpTestData(cls):
        users = populate_db(cls.USER_COUNT, cls.TIMELINES_PER_USER, 0, 0, 0)
        cls.user0 = User.objects.get(username=users[0]["username"])
        cls.user0_password = users[0]["password"]
        cls.new_historical_timeline_data = {
            "user": cls.user0,
            "title": "New Test Historical Timeline",
            "description": "Description",
            "scale_unit": 5,
            "scale_unit_length": 5,
            "page_size": "4",
            "page_orientation": "L",
            "page_scale_position": 0,
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get("/timelines/historical/add/")
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse("historical_timelines:timeline-add")
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse("historical_timelines:timeline-add")
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "historical_timelines/timeline_add.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("historical_timelines:timeline-add")
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_historical_timeline_added(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse("historical_timelines:timeline-add"),
            data=self.new_historical_timeline_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEquals(response.status_code, 200)

        historical_timelines = HistoricalTimeline.objects.filter(
            user=self.user0
        )
        expected_historical_timeline_count = self.TIMELINES_PER_USER + 1
        self.assertEquals(
            len(historical_timelines), expected_historical_timeline_count
        )

    def test_redirect_after_historical_timeline_added(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse("historical_timelines:timeline-add"),
            data=self.new_historical_timeline_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEquals(response.status_code, 200)

        historical_timeline = HistoricalTimeline.objects.get(
            title=self.new_historical_timeline_data["title"]
        )
        self.assertRedirects(
            response,
            reverse(
                "historical_timelines:timeline-detail",
                kwargs={"pk": historical_timeline.id},
            ),
            status_code=302,
        )
