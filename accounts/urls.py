from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views


app_name = "accounts"


urlpatterns = [
    path(
        "register/",
        views.register_request,
        name="register",
    ),
    path(
        "activate/<uidb64>/<token>",
        views.activate_request,
        name="activate",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            next_page="timelines:user-timelines",
        ),
        name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="accounts:login",
        ),
        name="logout"
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url=reverse_lazy("accounts:password-change-done")
        ),
        name="password-change",
    ),
    path(
        "password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="accounts/password_change_done.html",
        ),
        name="password-change-done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            success_url=reverse_lazy("accounts:password-reset-done")
        ),
        name="password_reset"
    ),
    path(
        "password_reset_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html"
        ),
        name="password-reset-done"
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password-reset-complete")
        ),
        name='password-reset-confirm'
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password-reset-complete"
    )
]
