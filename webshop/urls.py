from django.urls import path
from .views import (
    product_list,
    product_detail,
    checkout,
    process_checkout,
    profile,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("", product_list, name="product_list"),
    path("products/<int:product_id>/", product_detail, name="product_detail"),
    path("checkout/", checkout, name="checkout"),
    path("process_checkout/", process_checkout, name="process_checkout"),
    path("profile/<int:user_id>/", profile, name="profile"),
    path("password_reset/", password_reset, name="password_reset"),
    path("password_reset/done/", password_reset_done, name="password_reset_done"),
    path(
        "reset/<int:uid>/<token>/",
        password_reset_confirm,
        name="password_reset_confirm",
    ),
    path("reset/done/", password_reset_complete, name="password_reset_complete"),
]
