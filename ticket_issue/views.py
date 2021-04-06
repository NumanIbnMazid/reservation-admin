from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import TicketIssue
from util.helpers import (
    get_simple_object
)


class TicketIssueListView(ListView):
    template_name = "ticket-issue/issue-list.html"

    def get_queryset(self):
        qs = TicketIssue.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(
            TicketIssueListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Ticket Issue List'
        context['page_short_title'] = 'Ticket Issue List'
        context['list_objects'] = self.get_queryset()
        context['fields_count'] = len(TicketIssue._meta.get_fields()) + 2
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in TicketIssue._meta.fields + TicketIssue._meta.many_to_many])
        context['namespace'] = 'ticket-issue'
        context["detail_url"] = "ticket_issue:ticket_issue_detail"
        context['can_add_change'] = True if self.request.user.has_perm(
            'ticket_issue.add_ticketissue') == True and self.request.user.has_perm('ticket_issue.change_ticketissue') == True else False
        context['can_view'] = self.request.user.has_perm(
            'ticket_issue.view_ticketissue')
        context['can_delete'] = self.request.user.has_perm(
            'ticket_issue.delete_ticketissue')
        context['can_view_pnr'] = self.request.user.has_perm('pnr.view_pnr')
        return context


class TicketIssueDetailView(DetailView):
    template_name = "ticket-issue/issue-detail.html"

    def get_object(self):
        return get_simple_object(key='id', model=TicketIssue, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            TicketIssueDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'PNR - {self.get_object().pnr.pnr_no} Issued Ticket Detail'
        context['page_short_title'] = f'PNR - {self.get_object().pnr.pnr_no} Issued Ticket Detail'
        context["list_url"] = "ticket_issue:ticket_issue_list"
        context['can_add_change'] = True if self.request.user.has_perm(
            'ticket_issue.add_ticketissue') == True and self.request.user.has_perm('ticket_issue.change_ticketissue') == True else False
        context['can_view'] = self.request.user.has_perm(
            'ticket_issue.view_ticketissue')
        context['can_delete'] = self.request.user.has_perm(
            'ticket_issue.delete_ticketissue')
        context['can_view_pnr'] = self.request.user.has_perm('pnr.view_pnr')
        return context
