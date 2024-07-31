from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from historical_timelines.models import HistoricalTimeline
from timelines.models import Tag


class TagCreateViewTest(TestCase):
    USER_COUNT = 2
    TIMELINES_PER_USER = 1
    TAGS_PER_TIMELINE = 0

    @classmethod
    def setUpTestData(cls):
        users = populate_db(
            cls.USER_COUNT,
            cls.TIMELINES_PER_USER,
            0,
            0,
            cls.TAGS_PER_TIMELINE,
        )
        cls.user0 = User.objects.get(username=users[0]["username"])
        cls.user0_password = users[0]["password"]
        cls.user0_historical_timeline_id = users[0]["historical_timelines"][0][
            "id"
        ]
        historical_timeline = HistoricalTimeline.objects.get(
            id=cls.user0_historical_timeline_id
        )
        cls.user0_timeline_id = historical_timeline.timeline_ptr.pk
        cls.user1_historical_timeline_id = users[1]["historical_timelines"][0][
            "id"
        ]
        cls.new_tag_data = {
            "timeline": cls.user0_timeline_id,
            "name": "New Test Tag",
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            f"/timelines/historical/{self.user0_historical_timeline_id}"
            "/tag/add/"
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:tag-add",
                kwargs={
                    "historical_timeline_id": self.user0_historical_timeline_id
                },
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:tag-add",
                kwargs={
                    "historical_timeline_id": self.user0_historical_timeline_id
                },
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "historical_timelines/tag_add.html")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "historical_timelines:tag-add",
                kwargs={
                    "historical_timeline_id": self.user0_historical_timeline_id
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_forbidden_if_historical_timeline_not_owned_by_logged_in_user(
        self,
    ):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:tag-add",
                kwargs={
                    "historical_timeline_id": self.user1_historical_timeline_id
                },
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_tag_added(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "historical_timelines:tag-add",
                kwargs={
                    "historical_timeline_id": self.user0_historical_timeline_id
                },
            ),
            data=self.new_tag_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEquals(response.status_code, 200)

        tags = Tag.objects.filter(timeline=self.user0_timeline_id)
        expected_tag_count = self.TAGS_PER_TIMELINE + 1
        self.assertEquals(len(tags), expected_tag_count)

    def test_redirect_after_tag_added(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "historical_timelines:tag-add",
                kwargs={
                    "historical_timeline_id": self.user0_historical_timeline_id
                },
            ),
            data=self.new_tag_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse(
                "historical_timelines:timeline-detail",
                kwargs={"pk": self.user0_historical_timeline_id},
            ),
            status_code=302,
        )
