from django.urls import path, include
from .views import (
    PaymentListView, PaymentDetailsListView, PaymentDetailView, PaymentDetailsDetailView
)

urlpatterns = [
    path("get-payment-list/", PaymentListView.as_view(), name="payment_list"),
    path("get-payment-details-list/", PaymentDetailsListView.as_view(), name="payment_details_list"),
    path("payment/<id>/detail/", PaymentDetailView.as_view(), name="payment_detail"),
    path("payment-details/<id>/detail", PaymentDetailsDetailView.as_view(), name="payment_details_detail"),
]
