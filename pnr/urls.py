from django.urls import path, include
from .views import (
    PnrListView, PnrDetailsListView, PnrDetailView, PnrDetailsDetailView, issue_ticket, PnrDetailViewFromPNRno, PnrDetailsListViewFromPNRno
)


urlpatterns = [
    path("get-pnr-list/", PnrListView.as_view(), name="pnr_list"),
    path("get-pnr-details-list/", PnrDetailsListView.as_view(), name="pnr_details_list"),
    path("<id>/detail/", PnrDetailView.as_view(), name="pnr_detail"),
    path("<pnr_no>/detail/from-pnr-no/", PnrDetailViewFromPNRno.as_view(), name="pnr_detail_from_pnr_no"),
    path("pnr-details/<id>/detail/", PnrDetailsDetailView.as_view(), name="pnr_details_detail"),
    path("pnr-details/<pnr_no>/list/", PnrDetailsListViewFromPNRno.as_view(), name="pnr_details_list_from_pnr_no"),
    # Issue Ticket
    path("issue/air/ticket/", issue_ticket, name="issue_ticket"),
]
