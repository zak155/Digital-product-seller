from django.urls import path
from .views import product_list, product_detail
from .views import create_stripe_checkout_session,success_view,cancel_view
app_name = "products"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("<int:pk>/", product_detail, name="product_detail"),
    path(
        "create-checkout-session/<int:pk>/",
        create_stripe_checkout_session,
        name="create-checkout-session",
    ),
    path("success/", success_view, name="success"),
    path("cancel/", cancel_view, name="cancel"),
]