from django.shortcuts import render


def home(request):
    return render(
        request,
        "user_guide/home.html",
    )


def getting_started_index(request):
    return render(
        request,
        "user_guide/getting_started_index.html",
    )


def getting_started_age(request):
    return render(
        request,
        "user_guide/getting_started_age.html",
    )


def getting_started_date_time(request):
    return render(
        request,
        "user_guide/getting_started_date_time.html",
    )


def getting_started_historical(request):
    return render(
        request,
        "user_guide/getting_started_historical.html",
    )


def getting_started_scientific(request):
    return render(
        request,
        "user_guide/getting_started_scientific.html",
    )


def getting_started_scales(request):
    return render(
        request,
        "user_guide/getting_started_scales.html",
    )


def getting_started_orientation_size(request):
    return render(
        request,
        "user_guide/getting_started_orientation_size.html",
    )


def getting_started_positioning(request):
    return render(
        request,
        "user_guide/getting_started_positioning.html",
    )


def getting_started_sizing(request):
    return render(
        request,
        "user_guide/getting_started_sizing.html",
    )


def reference_index(request):
    return render(
        request,
        "user_guide/reference_index.html",
    )


def reference_timelines(request):
    return render(
        request,
        "user_guide/reference_timelines.html",
    )


def reference_events(request):
    return render(
        request,
        "user_guide/reference_events.html",
    )


def reference_event_areas(request):
    return render(
        request,
        "user_guide/reference_event_areas.html",
    )


def reference_tags(request):
    return render(
        request,
        "user_guide/reference_tags.html",
    )


def reference_age(request):
    return render(
        request,
        "user_guide/reference_age.html",
    )


def reference_date_time(request):
    return render(
        request,
        "user_guide/reference_date_time.html",
    )


def reference_historical(request):
    return render(
        request,
        "user_guide/reference_historical.html",
    )


def reference_scientific(request):
    return render(
        request,
        "user_guide/reference_scientific.html",
    )
