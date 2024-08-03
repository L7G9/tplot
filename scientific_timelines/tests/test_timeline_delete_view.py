from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from scientific_timelines.models import ScientificTimeline


class ScientificTimelineDeleteViewTest(TestCase):
    USER_COUNT = 2
    TIMELINES_PER_USER = 1

    @classmethod
    def setUpTestData(cls):
        users = populate_db(cls.USER_COUNT, cls.TIMELINES_PER_USER, 0, 0, 0)
        cls.user0 = User.objects.get(username=users[0]["username"])
        cls.user0_password = users[0]["password"]
        cls.user1 = User.objects.get(username=users[1]["username"])
        cls.user0_scientific_timeline_id = users[0]["scientific_timelines"][0][
            "id"
        ]
        cls.user1_scientific_timeline_id = users[1]["scientific_timelines"][0][
            "id"
        ]

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            f"/timelines/scientific/{self.user0_scientific_timeline_id}"
            "/delete/"
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-delete",
                kwargs={"pk": self.user0_scientific_timeline_id},
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
                "scientific_timelines:timeline-delete",
                kwargs={"pk": self.user0_scientific_timeline_id},
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "scientific_timelines/timeline_delete.html"
        )

    def test_context_object_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-delete",
                kwargs={"pk": self.user0_scientific_timeline_id},
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertTrue("object" in response.context)
        self.assertEqual(
            response.context["object"].get_owner(), response.context["user"]
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-delete",
                kwargs={"pk": self.user0_scientific_timeline_id},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_forbidden_if_scientific_timeline_not_owned_by_logged_in_user(
        self,
    ):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-delete",
                kwargs={"pk": self.user1_scientific_timeline_id},
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_scientific_timeline_deleted(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "scientific_timelines:timeline-delete",
                kwargs={"pk": self.user0_scientific_timeline_id},
            ),
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

        scientific_timelines = ScientificTimeline.objects.filter(
            user=self.user0
        )
        expected_scientific_timeline_count = self.TIMELINES_PER_USER - 1
        self.assertEqual(
            len(scientific_timelines), expected_scientific_timeline_count
        )

    def test_redirect_after_scientific_timeline_deleted(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "scientific_timelines:timeline-delete",
                kwargs={"pk": self.user0_scientific_timeline_id},
            ),
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, reverse("timelines:user-timelines"), status_code=302
        )
