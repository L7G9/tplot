from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path(
        "activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        views.activate_request,
        name="activate"
    ),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]
