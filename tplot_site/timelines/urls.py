from django.urls import path
from . import views


app_name = "timelines"

urlpatterns = [
    # ex: /timelines/
    path("", views.user_timelines, name="user_timelines"),
]
