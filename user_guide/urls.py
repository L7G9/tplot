from django.urls import path
from . import views


app_name = "user_guide"

urlpatterns = [
    # ex: /user_guide/
    path("", views.introduction, name="user-guide"),
    path("index.html", views.introduction, name="introduction"),
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
]
