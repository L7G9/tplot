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
        "activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        views.activate_request,
        name="activate",
    ),
    path(
        "login/",
        views.login_request,
        name="login"
    ),
    path(
        "logout/",
        views.logout_request,
        name="logout"
    ),
    path(
        "change_password/",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "change_password_done/",
        views.ChangePasswordDoneView.as_view(),
        name="change-password-done",
    ),

    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            success_url=reverse_lazy("accounts:password_reset_done")
        ),
        name='password_reset'
    ),
    path(
        'password_reset_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_sent.html"
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete")
        ),
        name='password_reset_confirm'
    ),
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name='password_reset_complete'
    )
]


temp = [
    path(
        "reset_password/",
        views.ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "reset_password_done/",
        views.ResetPasswordDoneView.as_view(),
        name="reset-password-done",
    ),

    path(
        "reset_password_confirm/",
        views.ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "reset_password_complete/",
        views.ResetPasswordCompleteView.as_view(),
        name="reset-password-complete",
    ),
]
