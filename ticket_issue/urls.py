from django.urls import path, include
from .views import (
    TicketIssueListView, TicketIssueDetailView
)


urlpatterns = [
    path("get-issued-ticket-list/",
         TicketIssueListView.as_view(), name="ticket_issue_list"),
    path("issued-ticket/<id>/detail/",
         TicketIssueDetailView.as_view(), name="ticket_issue_detail"),
]
