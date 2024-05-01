from django.shortcuts import render


def introduction(request):
    return render(
        request,
        "user_guide/index.html",
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


def e401(request):
    return render(
        request,
        "user_guide/401.html",
    )


def e404(request):
    return render(
        request,
        "user_guide/404.html",
    )


def e500(request):
    return render(
        request,
        "user_guide/500.html",
    )


def charts(request):
    return render(
        request,
        "user_guide/charts.html",
    )


def layout_sidenav_light(request):
    return render(
        request,
        "user_guide/layout-sidenav-light.html",
    )


def layout_static(request):
    return render(
        request,
        "user_guide/layout-static.html",
    )


def login(request):
    return render(
        request,
        "user_guide/login.html",
    )


def password(request):
    return render(
        request,
        "user_guide/password.html",
    )


def register(request):
    return render(
        request,
        "user_guide/register.html",
    )


def tables(request):
    return render(
        request,
        "user_guide/tables.html",
    )
