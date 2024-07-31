from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from historical_timelines.models import HistoricalTimeline


class HistoricalTimelineUpdateViewTest(TestCase):
    USER_COUNT = 2
    TIMELINES_PER_USER = 1

    @classmethod
    def setUpTestData(cls):
        users = populate_db(cls.USER_COUNT, cls.TIMELINES_PER_USER, 0, 0, 0)
        cls.user0 = User.objects.get(username=users[0]["username"])
        cls.user0_password = users[0]["password"]
        cls.user0_historical_timeline_id = users[0]["historical_timelines"][0][
            "id"
        ]
        cls.user1_historical_timeline_id = users[1]["historical_timelines"][0][
            "id"
        ]
        cls.updated_historical_timeline_data = {
            "user": cls.user0,
            "title": "Updated Historical Timeline",
            "description": "Description",
            "scale_unit": 5,
            "scale_length": 5,
            "page_size": "4",
            "page_orientation": "L",
            "page_scale_position": 0,
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:timeline-update",
                kwargs={"pk": self.user0_historical_timeline_id},
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:timeline-update",
                kwargs={"pk": self.user0_historical_timeline_id},
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
                "historical_timelines:timeline-update",
                kwargs={"pk": self.user0_historical_timeline_id},
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "historical_timelines/timeline_edit.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "historical_timelines:timeline-update",
                kwargs={"pk": self.user0_historical_timeline_id},
            )
        )
        timeline_id = self.user0_historical_timeline_id
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/timelines/historical/{timeline_id}"
            "/update/",
        )

    def test_forbidden_if_historical_timeline_not_owned_by_logged_in_user(
        self,
    ):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:timeline-update",
                kwargs={"pk": self.user1_historical_timeline_id},
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_historical_timeline_updated(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "historical_timelines:timeline-update",
                kwargs={"pk": self.user0_historical_timeline_id},
            ),
            data=self.updated_historical_timeline_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

        historical_timeline = HistoricalTimeline.objects.get(
            id=self.user0_historical_timeline_id
        )
        self.assertEqual(
            historical_timeline.title,
            self.updated_historical_timeline_data["title"],
        )

    def test_redirect_after_historical_timeline_updated(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "historical_timelines:timeline-update",
                kwargs={"pk": self.user0_historical_timeline_id},
            ),
            data=self.updated_historical_timeline_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse(
                "historical_timelines:timeline-detail",
                kwargs={"pk": self.user0_historical_timeline_id},
            ),
            status_code=302,
        )
