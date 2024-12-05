from django.urls import path
from .views import CreatePaymentView, cancel, index, stripe_webhook, success

urlpatterns = [
    path(
        "create-payment/<int:pk>/", CreatePaymentView.as_view(), name="create-payment"
    ),
    path(
        "webhooks/stripe/",
        stripe_webhook,
        name="stripe-webhook",
    ),
    path("", index, name="index"),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
]
