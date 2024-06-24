from django.urls import path
from . import views


app_name = "age_timelines"

urlpatterns = [
    # ex:1/detail/
    path(
        "<int:pk>/detail/",
        views.AgeTimelineDetailView.as_view(),
        name="age-timeline-detail",
    ),
    # ex: add/
    path(
        "add/", views.AgeTimelineCreateView.as_view(), name="age-timeline-add"
    ),
    # ex: 1/update/
    path(
        "<int:pk>/update/",
        views.AgeTimelineUpdateView.as_view(),
        name="age-timeline-update",
    ),
    # ex: 1/delete/
    path(
        "<int:pk>/delete/",
        views.AgeTimelineDeleteView.as_view(),
        name="age-timeline-delete",
    ),
    # ex: 1/event/add/
    path(
        "<int:age_timeline_id>/event/add/",
        views.AgeEventCreateView.as_view(),
        name="age-event-add",
    ),
    # ex: 1/event/1/update/
    path(
        "<int:age_timeline_id>/event/<int:pk>/update/",
        views.AgeEventUpdateView.as_view(),
        name="age-event-update",
    ),
    # ex: 1/event/delete/
    path(
        "<int:age_timeline_id>/event/<int:pk>/delete/",
        views.AgeEventDeleteView.as_view(),
        name="age-event-delete",
    ),
    # ex: 1/tag/add/
    path(
        "<int:age_timeline_id>/tag/add/",
        views.TagCreateView.as_view(),
        name="tag-add",
    ),
    # ex: 1/tag/1/update/
    path(
        "<int:age_timeline_id>/tag/<int:pk>/update/",
        views.TagUpdateView.as_view(),
        name="tag-update",
    ),
    # ex: 1/tag/1/delete/
    path(
        "<int:age_timeline_id>/tag/<int:pk>/delete/",
        views.TagDeleteView.as_view(),
        name="tag-delete",
    ),
    # ex: 1/event_area/add/
    path(
        "<int:age_timeline_id>/event_area/add/",
        views.EventAreaCreateView.as_view(),
        name="event-area-add",
    ),
    # ex: 1/event_area/1/update/
    path(
        "<int:age_timeline_id>/event_area/<int:pk>/update/",
        views.EventAreaUpdateView.as_view(),
        name="event-area-update",
    ),
    # ex: 1/event_area/1/delete/
    path(
        "<int:age_timeline_id>/event_area/<int:pk>/delete/",
        views.EventAreaDeleteView.as_view(),
        name="event-area-delete",
    ),
    # ex: 1/pdf/
    path(
        "<int:age_timeline_id>/pdf/",
        views.pdf_view,
        name="age-timeline-pdf",
    ),
    # ex: 1/ai_request/
    path(
        "<int:age_timeline_id>/ai_request/",
        views.AIRequestView.as_view(),
        name="ai-request",
    ),
    # ex: 1/ai_result/
    path(
        "<int:age_timeline_id>/ai_result/",
        views.AIResultView.as_view(),
        name="ai-result",
    ),
]
