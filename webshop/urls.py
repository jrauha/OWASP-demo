from django.urls import path
from .views import product_list, product_detail, checkout, process_checkout, profile
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("", product_list, name="product_list"),
    path("products/<int:product_id>/", product_detail, name="product_detail"),
    path("checkout/", checkout, name="checkout"),
    path("process_checkout/", process_checkout, name="process_checkout"),
    path("profile/", profile, name="profile"),
]
