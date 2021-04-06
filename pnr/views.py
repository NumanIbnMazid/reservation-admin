from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import PNR, PnrDetails
from util.helpers import (
    get_simple_object
)
import requests
from decouple import config, Csv
import json
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


class PnrListView(ListView):
    template_name = "pnr/pnr-list.html"

    def get_queryset(self):
        qs = PNR.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(
            PnrListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Passenger Name Record (PNR) List'
        context['page_short_title'] = 'PNR List'
        context['list_objects'] = self.get_queryset()
        context['fields_count'] = len(PNR._meta.get_fields()) + 2
        context['fields'] = dict([(f.name, f.verbose_name) for f in PNR._meta.fields + PNR._meta.many_to_many])
        context['namespace'] = 'pnr'
        context["detail_url"] = "pnr:pnr_detail"
        context["label_to_skip"] = ["utils", "sabre_token"]
        context['can_add_change'] = True if self.request.user.has_perm(
            'pnr.add_pnr') == True and self.request.user.has_perm('pnr.change_pnr') == True else False
        context['can_view'] = self.request.user.has_perm('pnr.view_pnr')
        context['can_view_pnr_details'] = self.request.user.has_perm('pnr.view_pnrdetails')
        context['can_delete'] = self.request.user.has_perm('pnr.delete_pnr')
        return context


class PnrDetailsListView(ListView):
    template_name = "pnr/pnr-detail-list.html"

    def get_queryset(self):
        qs = PnrDetails.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(
            PnrDetailsListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Passenger Name Record (PNR) Details List'
        context['page_short_title'] = 'PNR Details List'
        context['list_objects'] = self.get_queryset()
        context['fields_count'] = len(PnrDetails._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name) for f in PnrDetails._meta.fields + PnrDetails._meta.many_to_many])
        context['namespace'] = 'pnr-details'
        context["detail_url"] = "pnr:pnr_details_detail"
        context['can_add_change'] = True if self.request.user.has_perm(
            'pnr.add_pnrdetails') == True and self.request.user.has_perm('pnr.change_pnrdetails') == True else False
        context['can_view'] = self.request.user.has_perm('pnr.view_pnrdetails')
        context['can_view_pnr'] = self.request.user.has_perm('pnr.view_pnr')
        context['can_delete'] = self.request.user.has_perm('pnr.delete_pnrdetails')
        return context


class PnrDetailView(DetailView):
    template_name = "pnr/pnr-detail.html"

    def get_object(self):
        return get_simple_object(key='id', model=PNR, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            PnrDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'PNR - {self.get_object().pnr_no} Detail'
        context['page_short_title'] = f'PNR - {self.get_object().pnr_no} Detail'
        context["list_url"] = "pnr:pnr_list"
        context['can_add_change'] = True if self.request.user.has_perm('pnr.add_pnr') == True and self.request.user.has_perm('pnr.change_pnr') == True else False
        context['can_view'] = self.request.user.has_perm('pnr.view_pnr')
        context['can_view_pnr_details'] = self.request.user.has_perm('pnr.view_pnrdetails')
        context['can_delete'] = self.request.user.has_perm('pnr.delete_pnr')
        context['can_view_ticket_issue'] = self.request.user.has_perm(
            'ticket_issue.view_ticketissue')
        return context


class PnrDetailViewFromPNRno(DetailView):
    template_name = "pnr/pnr-detail.html"

    def get_object(self):
        qs = PNR.objects.filter(pnr_no=self.kwargs["pnr_no"])
        if qs.exists():
            return qs.first()
        return None

    def get_context_data(self, **kwargs):
        context = super(
            PnrDetailViewFromPNRno, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'PNR - {self.get_object().pnr_no} Detail'
        context['page_short_title'] = f'PNR - {self.get_object().pnr_no} Detail'
        context["list_url"] = "pnr:pnr_list"
        context['can_add_change'] = True if self.request.user.has_perm('pnr.add_pnr') == True and self.request.user.has_perm('pnr.change_pnr') == True else False
        context['can_view'] = self.request.user.has_perm('pnr.view_pnr')
        context['can_view_pnr_details'] = self.request.user.has_perm('pnr.view_pnrdetails')
        context['can_delete'] = self.request.user.has_perm('pnr.delete_pnr')
        context['can_view_ticket_issue'] = self.request.user.has_perm(
            'ticket_issue.view_ticketissue')
        return context


class PnrDetailsDetailView(DetailView):
    template_name = "pnr/pnr-details-detail.html"

    def get_object(self):
        return get_simple_object(key='id', model=PnrDetails, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            PnrDetailsDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'PNR - {self.get_object().pnr.pnr_no} Detail'
        context['page_short_title'] = f'PNR - {self.get_object().pnr.pnr_no} Detail'
        context["list_url"] = "pnr:pnr_list"
        context['can_add_change'] = True if self.request.user.has_perm(
            'pnr.add_pnrdetails') == True and self.request.user.has_perm('pnr.change_pnrdetails') == True else False
        context['can_view'] = self.request.user.has_perm('pnr.view_pnrdetails')
        context['can_view_pnr'] = self.request.user.has_perm('pnr.view_pnr')
        context['can_view_pnr_details'] = self.request.user.has_perm('pnr.view_pnrdetails')
        context['can_delete'] = self.request.user.has_perm('pnr.delete_pnrdetails')
        return context


class PnrDetailsListViewFromPNRno(ListView):
    template_name = "pnr/pnr-detail-list.html"

    def get_queryset(self):
        qs = PnrDetails.objects.filter(pnr__pnr_no=self.kwargs["pnr_no"])
        if qs.exists():
            return qs
        return None

    def get_context_data(self, **kwargs):
        context = super(
            PnrDetailsListViewFromPNRno, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Passenger Name Record (PNR) Details List'
        context['page_short_title'] = 'PNR Details List'
        context['list_objects'] = self.get_queryset()
        context['fields_count'] = len(PnrDetails._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name) for f in PnrDetails._meta.fields + PnrDetails._meta.many_to_many])
        context['namespace'] = 'pnr_details'
        context["detail_url"] = "pnr:pnr_details_detail"
        context['can_add_change'] = True if self.request.user.has_perm(
            'pnr.add_pnrdetails') == True and self.request.user.has_perm('pnr.change_pnrdetails') == True else False
        context['can_view'] = self.request.user.has_perm('pnr.view_pnrdetails')
        context['can_view_pnr'] = self.request.user.has_perm('pnr.view_pnr')
        context['can_delete'] = self.request.user.has_perm('pnr.delete_pnrdetails')
        return context


def issue_ticket(request):
    if request.user.has_perm('ticket_issue.add_ticketissue') == True:
        if request.method == "POST":
            pnr_no = request.POST.get("pnr_no")
            
            skytrip_production_status = config('SKYTRIP_IS_IN_PRODUCTION', default=False, cast=bool)

            if skytrip_production_status == True:
                endpoint = config('ISSUE_TICKET_ENDPOINT_PROD')
                api_key = config('ISSUE_TICKET_API_KEY_PROD')
            else:
                endpoint = config('ISSUE_TICKET_ENDPOINT_DEV')
                api_key = config('ISSUE_TICKET_API_KEY_DEV')

            pnr_qs = PNR.objects.filter(
                pnr_no=pnr_no
            )

            if pnr_qs.exists():
                pnr = pnr_qs.first()

                body = {
                    "ExistedToken": pnr.sabre_token,
                    "RequestBody": {
                        "ItineraryID": pnr.pnr_no
                    }
                }
                headers = {
                    'content-type': 'application/json',
                    'x-api-key': api_key
                }

                res = requests.post(
                    endpoint, data=json.dumps(body), headers=headers
                )

                response = res.json()

                if response["statusCode"] == 200 and response["body"]["responseData"]["AirTicketRS"]["ApplicationResults"].get("status", None) == "Complete":
                    messages.add_message(request, messages.SUCCESS,
                                        f'Tikcket Issued Successfully! PNR No: {pnr_no}!')
                else:
                    messages.add_message(request, messages.ERROR,
                                        f"Failed to Issue Air Ticket!")

            else:
                messages.add_message(request, messages.ERROR,
                                    f'Failed to find the PNR {pnr_no}!')

            return HttpResponseRedirect(reverse("pnr:pnr_list"))
    else:
        messages.add_message(request, messages.ERROR,
                             f"Not enough permission to view the content!")
        return HttpResponseRedirect(reverse("home"))
