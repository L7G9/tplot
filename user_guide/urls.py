from django.urls import path
from . import views


app_name = "user_guide"

urlpatterns = [
    # ex: /user_guide/
    path("", views.home, name="home"),
    path("home.html", views.home, name="introduction"),
    path(
        "getting_started_index.html",
        views.getting_started_index,
        name="getting-started-index"
    ),
    path(
        "getting_started_age.html",
        views.getting_started_age,
        name="getting-started-age"
    ),
    path(
        "getting_started_date_time.html",
        views.getting_started_date_time,
        name="getting-started-date-time"
    ),
    path(
        "getting_started_historical.html",
        views.getting_started_historical,
        name="getting-started-historical"
    ),
    path(
        "getting_started_scientific.html",
        views.getting_started_scientific,
        name="getting-started-scientific"
    ),
    path(
        "getting_started_scales.html",
        views.getting_started_scales,
        name="getting-started-scales"
    ),
    path(
        "getting_started_orientation_size.html",
        views.getting_started_orientation_size,
        name="getting-started-orientation-size"
    ),
    path(
        "getting_started_positioning.html",
        views.getting_started_positioning,
        name="getting-started-positioning"
    ),
    path(
        "getting_started_sizing.html",
        views.getting_started_sizing,
        name="getting-started-sizing"
    ),
    path(
        "reference_index.html",
        views.reference_index,
        name="reference-index"
    ),
    path(
        "reference_timelines.html",
        views.reference_timelines,
        name="reference-timelines"
    ),
    path(
        "reference_events.html",
        views.reference_events,
        name="reference-events"
    ),
    path(
        "reference_event_areas.html",
        views.reference_event_areas,
        name="reference-event-areas"
    ),
    path(
        "reference_tags.html",
        views.reference_tags,
        name="reference-tags"
    ),
    path(
        "reference_age.html",
        views.reference_age,
        name="reference-age"
    ),
    path(
        "reference_date_time.html",
        views.reference_date_time,
        name="reference-date-time"
    ),
    path(
        "reference_historical.html",
        views.reference_historical,
        name="reference-historical"
    ),
    path(
        "reference_scientific.html",
        views.reference_scientific,
        name="reference-scientific"
    ),
]
