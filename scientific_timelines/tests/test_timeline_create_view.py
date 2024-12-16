from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from scientific_timelines.models import ScientificTimeline


class ScientificTimelineCreateViewTest(TestCase):
    USER_COUNT = 1
    TIMELINES_PER_USER = 0

    @classmethod
    def setUpTestData(cls):
        users = populate_db(cls.USER_COUNT, cls.TIMELINES_PER_USER, 0, 0, 0)
        cls.user0 = User.objects.get(username=users[0]["username"])
        cls.user0_password = users[0]["password"]
        cls.new_scientific_timeline_data = {
            "user": cls.user0,
            "title": "New Test Scientific Timeline",
            "description": "Description",
            "scale_unit": 1000,
            "scale_unit_length": 5,
            "pdf_page_size": "4",
            "page_orientation": "L",
            "page_scale_position": 0,
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get("/timelines/scientific/add/")
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse("scientific_timelines:timeline-add")
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse("scientific_timelines:timeline-add")
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "scientific_timelines/timeline_add.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("scientific_timelines:timeline-add")
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_scientific_timeline_added(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse("scientific_timelines:timeline-add"),
            data=self.new_scientific_timeline_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEquals(response.status_code, 200)

        scientific_timelines = ScientificTimeline.objects.filter(
            user=self.user0
        )
        expected_scientific_timeline_count = self.TIMELINES_PER_USER + 1
        self.assertEquals(
            len(scientific_timelines), expected_scientific_timeline_count
        )

    def test_redirect_after_scientific_timeline_added(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse("scientific_timelines:timeline-add"),
            data=self.new_scientific_timeline_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEquals(response.status_code, 200)

        scientific_timeline = ScientificTimeline.objects.get(
            title=self.new_scientific_timeline_data["title"]
        )
        self.assertRedirects(
            response,
            reverse(
                "scientific_timelines:timeline-detail",
                kwargs={"pk": scientific_timeline.id},
            ),
            status_code=302,
        )
