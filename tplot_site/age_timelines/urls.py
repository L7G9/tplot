from django.urls import path
from . import views


app_name = "age_timelines"

urlpatterns = [
    # ex: /edit/1/
    path("edit/<int:age_timeline_id>/", views.age_timeline_edit, name="age_timeline_edit"),
]
