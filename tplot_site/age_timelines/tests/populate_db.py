from django.contrib.auth.models import User
from age_timelines.models import AgeEvent, AgeTimeline
from timelines.models import EventArea, Tag


def populate_db(users, age_timelines, age_events, tags, areas):
    for user_index in range(users):
        user = User.objects.create_user(
            username=f"test_user_{user_index}",
            password=f"TestUser{user_index}#"
        )
        for age_timeline_index in range(age_timelines):
            age_timeline = AgeTimeline.objects.create(user=user, title=f"{user.username} AgeTimeline {age_timeline_index}")
            for age_event_index in range(age_events):
                AgeEvent.objects.create(age_timeline=age_timeline, timeline_id=age_timeline.timeline_ptr.pk, title=f"event {age_event_index}")
            for tag_index in range(tags):
                Tag.objects.create(timeline=age_timeline.timeline_ptr, name=f"tag {tag_index}")
            for area_index in range(areas):
                EventArea.objects.create(timeline=age_timeline.timeline_ptr, name=f"area {area_index}", page_position=area_index+1)
