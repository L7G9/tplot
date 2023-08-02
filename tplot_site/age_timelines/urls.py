from django.urls import path
from . import views


app_name = "age_timelines"

urlpatterns = [
    # ex:1/detail/
    path("<int:pk>/detail/", views.AgeTimelineDetailView.as_view(), name="age-timeline-detail"),
    # ex: add/
    path("add/", views.AgeTimelineCreateView.as_view(), name="age-timeline-add"),
    # ex: 1/update/
    path("<int:pk>/update/", views.AgeTimelineUpdateView.as_view(), name="age-timeline-update"),
    # ex: 1/delete/
    path("<int:pk>/delete/", views.AgeTimelineDeleteView.as_view(), name="age-timeline-delete"),
    # ex: 1/event/add/
    path("<int:age_timeline_id>/event/add/", views.AgeEventCreateView.as_view(), name="age-event-add"),
    # ex: event/1/update/
    path("event/<int:pk>/update/", views.AgeEventUpdateView.as_view(), name="age-event-update"),
    # ex: event/delete/
    path("event/<int:pk>/delete/", views.AgeEventDeleteView.as_view(), name="age-event-delete"),
]