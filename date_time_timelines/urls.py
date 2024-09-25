from django.urls import path
from . import views


app_name = "date_time_timelines"

urlpatterns = [
    # ex:1/detail/
    path(
        "<int:pk>/detail/",
        views.DateTimeTimelineDetailView.as_view(),
        name="date-time-timeline-detail",
    ),
    # ex: add/
    path(
        "add/",
        views.DateTimeTimelineCreateView.as_view(),
        name="date-time-timeline-add"
    ),
    # ex: 1/update/
    path(
        "<int:pk>/update/",
        views.DateTimeTimelineUpdateView.as_view(),
        name="date-time-timeline-update",
    ),
    # ex: 1/delete/
    path(
        "<int:pk>/delete/",
        views.DateTimeTimelineDeleteView.as_view(),
        name="date-time-timeline-delete",
    ),
    # ex: 1/event/add/
    path(
        "<int:date_time_timeline_id>/event/add/",
        views.DateTimeEventCreateView.as_view(),
        name="date-time-event-add",
    ),
    # ex: 1/event/1/update/
    path(
        "<int:date_time_timeline_id>/event/<int:pk>/update/",
        views.DateTimeEventUpdateView.as_view(),
        name="date-time-event-update",
    ),
    # ex: 1/event/1/delete/
    path(
        "<int:date_time_timeline_id>/event/<int:pk>/delete/",
        views.DateTimeEventDeleteView.as_view(),
        name="date-time-event-delete",
    ),
    # ex: 1/tag/add/
    path(
        "<int:date_time_timeline_id>/tag/add/",
        views.TagCreateView.as_view(),
        name="tag-add",
    ),
    # ex: 1/tag/1/update/
    path(
        "<int:date_time_timeline_id>/tag/<int:pk>/update/",
        views.TagUpdateView.as_view(),
        name="tag-update",
    ),
    # ex: 1/tag/1/delete/
    path(
        "<int:date_time_timeline_id>/tag/<int:pk>/delete/",
        views.TagDeleteView.as_view(),
        name="tag-delete",
    ),
    # ex: 1/event_area/add/
    path(
        "<int:date_time_timeline_id>/event_area/add/",
        views.EventAreaCreateView.as_view(),
        name="event-area-add",
    ),
    # ex: 1/event_area/1/update/
    path(
        "<int:date_time_timeline_id>/event_area/<int:pk>/update/",
        views.EventAreaUpdateView.as_view(),
        name="event-area-update",
    ),
    # ex: 1/event_area/1/delete/
    path(
        "<int:date_time_timeline_id>/event_area/<int:pk>/delete/",
        views.EventAreaDeleteView.as_view(),
        name="event-area-delete",
    ),

    # ex: 1/collaborators/
    path(
        "<int:pk>/collaborators/",
        views.CollaboratorsView.as_view(),
        name="collaborators",
    ),
    # ex: 1/collaborator/add/
    path(
        "<int:date_time_timeline_id>/collaborator/add/",
        views.CollaboratorCreateView.as_view(),
        name="collaborator-add",
    ),
    # ex: 1/collaborator/1/update/
    path(
        "<int:date_time_timeline_id>/collaborator/<int:pk>/update/",
        views.CollaboratorUpdateView.as_view(),
        name="collaborator-update",
    ),
    # ex: 1/collaborator/1/delete/
    path(
        "<int:date_time_timeline_id>/collaborator/<int:pk>/delete/",
        views.CollaboratorDeleteView.as_view(),
        name="collaborator-delete",
    ),

    # ex: 1/timeline/
    path(
        "<int:pk>/timeline/",
        views.TimelineView.as_view(),
        name="timeline",
    ),
    # ex: 1/pdf/
    path(
        "<int:date_time_timeline_id>/pdf/",
        views.pdf_view,
        name="date-time-timeline-pdf",
    ),
    # ex: 1/ai_request/
    path(
        "<int:date_time_timeline_id>/ai_request/",
        views.AIRequestView.as_view(),
        name="date-time-timeline-ai-request",
    ),
    # ex: 1/ai_result/
    path(
        "<int:date_time_timeline_id>/ai_result/",
        views.AIResultView.as_view(),
        name="date-time-timeline-ai-result",
    ),
]
