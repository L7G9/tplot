from django.urls import path
from . import views


app_name = "historical_timelines"

urlpatterns = [
    # ex:1/detail/
    path(
        "<int:pk>/detail/",
        views.TimelineDetailView.as_view(),
        name="timeline-detail",
    ),
    # ex: add/
    path(
        "add/",
        views.TimelineCreateView.as_view(),
        name="timeline-add"
    ),
    # ex: 1/update/
    path(
        "<int:pk>/update/",
        views.TimelineUpdateView.as_view(),
        name="timeline-update",
    ),
    # ex: 1/delete/
    path(
        "<int:pk>/delete/",
        views.TimelineDeleteView.as_view(),
        name="timeline-delete",
    ),
    # ex: 1/event/add/
    path(
        "<int:historical_timeline_id>/event/add/",
        views.EventCreateView.as_view(),
        name="event-add",
    ),
    # ex: 1/event/1/update/
    path(
        "<int:historical_timeline_id>/event/<int:pk>/update/",
        views.EventUpdateView.as_view(),
        name="event-update",
    ),
    # ex: 1/event/delete/
    path(
        "<int:historical_timeline_id>/event/<int:pk>/delete/",
        views.EventDeleteView.as_view(),
        name="event-delete",
    ),
    # ex: 1/tag/add/
    path(
        "<int:historical_timeline_id>/tag/add/",
        views.TagCreateView.as_view(),
        name="tag-add",
    ),
    # ex: 1/tag/1/update/
    path(
        "<int:historical_timeline_id>/tag/<int:pk>/update/",
        views.TagUpdateView.as_view(),
        name="tag-update",
    ),
    # ex: 1/tag/1/delete/
    path(
        "<int:historical_timeline_id>/tag/<int:pk>/delete/",
        views.TagDeleteView.as_view(),
        name="tag-delete",
    ),
    # ex: 1/event_area/add/
    path(
        "<int:historical_timeline_id>/event_area/add/",
        views.EventAreaCreateView.as_view(),
        name="event-area-add",
    ),
    # ex: 1/event_area/1/update/
    path(
        "<int:historical_timeline_id>/event_area/<int:pk>/update/",
        views.EventAreaUpdateView.as_view(),
        name="event-area-update",
    ),
    # ex: 1/event_area/1/delete/
    path(
        "<int:scientific_timeline_id>/event_area/<int:pk>/delete/",
        views.EventAreaDeleteView.as_view(),
        name="event-area-delete",
    ),
    # ex: 1/timeline/
    path(
        "<int:pk>/timeline/",
        views.TimelineView.as_view(),
        name="timeline",
    ),
    # ex: 1/pdf/
    path(
        "<int:historical_timeline_id>/pdf/",
        views.pdf_view,
        name="timeline-pdf",
    )
]
