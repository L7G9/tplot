from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db


class ScientificTimelineDetailViewTest(TestCase):
    USER_COUNT = 2
    TIMELINES_PER_USER = 1
    EVENTS_PER_TIMELINE = 6
    TAGS_PER_TIMELINE = 3
    AREAS_PER_TIMELINE = 2

    @classmethod
    def setUpTestData(cls):
        users = populate_db(
            cls.USER_COUNT,
            cls.TIMELINES_PER_USER,
            cls.EVENTS_PER_TIMELINE,
            cls.TAGS_PER_TIMELINE,
            cls.AREAS_PER_TIMELINE,
        )
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
            "/detail/"
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-detail",
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
                "scientific_timelines:timeline-detail",
                kwargs={"pk": self.user0_scientific_timeline_id},
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "scientific_timelines/timeline_detail.html"
        )

    def test_context_scientific_timeline_object_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-detail",
                kwargs={"pk": self.user0_scientific_timeline_id},
            )
        )
        self.assertTrue("object" in response.context)
        self.assertEqual(
            response.context["object"].get_owner(), response.context["user"]
        )

    def test_scientific_events_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-detail",
                kwargs={"pk": self.user0_scientific_timeline_id},
            )
        )
        scientific_events = response.context[
            "object"
        ].scientificevent_set.all()
        self.assertEqual(len(scientific_events), self.EVENTS_PER_TIMELINE)
        for scientific_Event in scientific_events:
            self.assertEqual(
                scientific_Event.get_owner(), response.context["user"]
            )

    def test_tags_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-detail",
                kwargs={"pk": self.user0_scientific_timeline_id},
            )
        )
        tags = response.context["object"].tag_set.all()
        self.assertEqual(len(tags), self.TAGS_PER_TIMELINE)
        for tag in tags:
            self.assertEqual(tag.get_owner(), response.context["user"])

    def test_event_areas_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-detail",
                kwargs={"pk": self.user0_scientific_timeline_id},
            )
        )
        areas = response.context["object"].eventarea_set.all()
        self.assertEqual(len(areas), self.AREAS_PER_TIMELINE)
        for area in areas:
            self.assertEqual(area.get_owner(), response.context["user"])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "scientific_timelines:timeline-detail",
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
                "scientific_timelines:timeline-detail",
                kwargs={"pk": self.user1_scientific_timeline_id},
            )
        )
        self.assertEqual(response.status_code, 403)
