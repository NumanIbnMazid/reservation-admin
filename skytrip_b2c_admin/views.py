from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
# import models
from pnr.models import PNR, PNRcarrierCodeStats
from ticket_issue.models import TicketIssue
from payment.models import Payment
from user.models import SkytripUser
from django.contrib.auth.models import User, Group, Permission
import datetime
import json
import math
import random


@login_required
def home(request):
    return render(request, 'pages/dashboard.html')


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = "pages/dashboard.html"

    def get_rgba_colors(self):
        colors = {
            "1": ["Red", "rgba(255,0,0,0.2)", "rgba(255,0,0,1)"],
            "2": ["Lime", "rgba(0,255,0,0.2)", "rgba(0,255,0,1)"],
            "3": ["Blue", "rgba(0,0,255,0.2)", "rgba(0,0,255,1)"],
            "4": ["Yellow", "rgba(255,255,0,0.2)", "rgba(255,255,0,1)"],
            "5": ["Aqua", "rgba(0,255,255,0.2)", "rgba(0,255,255,1)"],
            "6": ["Fuchsia", "rgba(255,0,255,0.2)", "rgba(255,0,255,1)"],
            "7": ["Silver", "rgba(192,192,192,0.2)", "rgba(192,192,192,1)"],
            "8": ["Gray", "rgba(128,128,128,0.2)", "rgba(128,128,128,1)"],
            "9": ["Maroon", "rgba(128,0,0,0.2)", "rgba(128,0,0,1)"],
            "10": ["Olive", "rgba(128,128,0,0.2)", "rgba(128,128,0,1)"],
            "11": ["Green", "rgba(0,128,0,0.2)", "rgba(0,128,0,1)"],
            "12": ["Purple", "rgba(128,0,128,0.2)", "rgba(128,0,128,1)"],
            "13": ["Teal", "rgba(0,128,128,0.2)", "rgba(0,128,128,1)"],
            "14": ["Navy", "rgba(0,0,128,0.2)", "rgba(0,0,128,1)"],
            "15": ["Maroon", "rgba(128,0,0,0.2)", "rgba(128,0,0,1)"],
            "16": ["Brown", "rgba(165,42,42,0.2)", "rgba(165,42,42,1)"],
            "17": ["Crimson", "rgba(220,20,60,0.2)", "rgba(220,20,60,1)"],
            "18": ["Tomato", "rgba(255,99,71,0.2)", "rgba(255,99,71,1)"],
            "19": ["Coral", "rgba(255,127,80,0.2)", "rgba(255,127,80,1)"],
            "20": ["Indian Red", "rgba(205,92,92,0.2)", "rgba(205,92,92,1)"],
            "21": ["light Coral", "rgba(240,128,128,0.2)", "rgba(240,128,128,1)"],
            "22": ["Dark Salmon", "rgba(233,150,122,0.2)", "rgba(233,150,122,1)"],
            "23": ["Salmon", "rgba(250,128,114,0.2)", "rgba(250,128,114,1)"],
            "24": ["Light Salmon", "rgba(255,160,122,0.2)", "rgba(255,160,122,1)"],
            "25": ["Orange Red", "rgba(255,69,0,0.2)", "rgba(255,69,0,1)"],
            "26": ["Dark Orange", "rgba(255,140,0,0.2)", "rgba(255,140,0,1)"],
            "27": ["Orange", "rgba(255,165,0,0.2)", "rgba(255,165,0,1)"],
            "28": ["Gold", "rgba(255,215,0,0.2)", "rgba(255,215,0,1)"],
            "29": ["Dark Golden Rod", "rgba(184,134,11,0.2)", "rgba(184,134,11,1)"],
            "30": ["Golden Rod", "rgba(218,165,32,0.2)", "rgba(218,165,32,1)"],
            "31": ["Pale Golden Rod", "rgba(238,232,170,0.2)", "rgba(238,232,170,1)"],
            "32": ["Dark Khaki", "rgba(189,183,107,0.2)", "rgba(189,183,107,1)"],
            "33": ["Khaki", "rgba(240,230,140,0.2)", "rgba(240,230,140,1)"],
            "34": ["Olive", "rgba(128,128,0,0.2)", "rgba(128,128,0,1)"],
            "35": ["Yellow", "rgba(255,255,0,0.2)", "rgba(255,255,0,1)"],
            "36": ["Yellow Green", "rgba(154,205,50,0.2)", "rgba(154,205,50,1)"],
            "37": ["Dark Olive Green", "rgba(85,107,47,0.2)", "rgba(85,107,47,1)"],
            "38": ["Olive Drab", "rgba(107,142,35,0.2)", "rgba(107,142,35,1)"],
            "39": ["Lawn Green", "rgba(124,252,0,0.2)", "rgba(124,252,0,1)"],
            "40": ["Chart Reuse", "rgba(127,255,0,0.2)", "rgba(127,255,0,1)"],
        }
        return colors

    def get_context_data(self, **kwargs):
        context = super(
            HomeView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Dashboard'
        context['page_short_title'] = 'Dashboard'

        # pass rgba colors
        context['rgba_colors'] = json.dumps(self.get_rgba_colors())

        # Object Counters
        context['pnrs_count'] = PNR.objects.all().count()
        context['issued_tickets_count'] = TicketIssue.objects.all().count()
        context['payments_count'] = Payment.objects.all().count()
        context['skytrip_users_count'] = SkytripUser.objects.all().count()
        context['admin_users_count'] = User.objects.all().count()
        context['user_groups_count'] = Group.objects.all().count()
        context['user_permissions_count'] = Permission.objects.all().count()

        # Report Data Starts
        query_context_date_from = self.request.GET.get('from_date')
        query_context_date_to = self.request.GET.get('to_date')
        context['query_date_from'] = query_context_date_from
        context['query_date_to'] = query_context_date_to
        request = self.request
        method_dict = request.GET
        date_from_filtered = method_dict.get('from_date', None)
        date_to_filtered = method_dict.get('to_date', None)

        # finalize to datetime
        if date_to_filtered is not None and date_to_filtered is not "":
            date_to_filtered = datetime.datetime.strptime(date_to_filtered + " 23:59:59", '%Y-%m-%d %H:%M:%S')

        if date_from_filtered == None or date_from_filtered == "":
            date_from_filtered = "1990-01-01 00:00:00"

        if date_to_filtered == None or date_to_filtered == "":
            date_to_filtered = datetime.datetime.now()

        if date_from_filtered is not None and date_from_filtered is not "":
            # ------- PNR -------
            context['pnr_date_filtered'] = PNR.objects.filter(created_at__range=(date_from_filtered, date_to_filtered))
            context['pnr_date_filtered_count'] = PNR.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).count()
            context['pnr_fields_count'] = len(PNR._meta.get_fields()) + 2
            context['pnr_fields'] = dict([(f.name, f.verbose_name) for f in PNR._meta.fields + PNR._meta.many_to_many])
            context['skip_labels'] = ["utils", "sabre_token"]
            context['can_view_pnr'] = self.request.user.has_perm('pnr.view_pnr')
            # ------- PNR B2C -------
            context['pnr_b2c_date_filtered'] = PNR.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(data_source__iexact="B2C")
            context['pnr_b2c_date_filtered_count'] = PNR.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(data_source__iexact="B2C").count()
            # ------- PNR B2B -------
            context['pnr_b2b_date_filtered'] = PNR.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(data_source__iexact="B2B")
            context['pnr_b2b_date_filtered_count'] = PNR.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(data_source__iexact="B2B").count()
            # ------- PNR Carrier Code Stats -------
            context['pnr_carrier_code_stats_date_filtered'] = PNRcarrierCodeStats.objects.filter(created_at__range=(date_from_filtered, date_to_filtered))
            carrier_code_stats_dict = {}
            for carrier_stats in PNRcarrierCodeStats.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)):
                carrier_code_stats_dict[carrier_stats.carrier_code] = carrier_stats.number_of_pnrs
            context['carrier_code_stats_dict'] = json.dumps(carrier_code_stats_dict)
            context['pnr_carrier_code_stats_date_filtered_count'] = PNRcarrierCodeStats.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).count()
            context['pnr_carrier_code_stats_fields_count'] = len(PNRcarrierCodeStats._meta.get_fields()) + 2
            context['pnr_carrier_code_stats_fields'] = dict([(f.name, f.verbose_name) for f in PNRcarrierCodeStats._meta.fields + PNRcarrierCodeStats._meta.many_to_many])
            context['can_view_pnr_carrier_code_stats'] = self.request.user.has_perm('pnr.view_pnrcarriercodestats')
            # ------- Ticket Issue -------
            context['ticket_issue_date_filtered'] = TicketIssue.objects.filter(created_at__range=(date_from_filtered, date_to_filtered))
            context['ticket_issue_date_filtered_count'] = TicketIssue.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).count()
            context['ticket_issue_fields_count'] = len(TicketIssue._meta.get_fields()) + 2
            context['ticket_issue_fields'] = dict([(f.name, f.verbose_name) for f in TicketIssue._meta.fields + TicketIssue._meta.many_to_many])
            context['can_view_ticket_issue'] = self.request.user.has_perm('ticket_issue.view_ticketissue')
            # ------- Ticket Issue B2C -------
            context['ticket_issue_b2c_date_filtered'] = TicketIssue.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(pnr__data_source__iexact="B2C")
            context['ticket_issue_b2c_date_filtered_count'] = TicketIssue.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(pnr__data_source__iexact="B2C").count()
            # ------- Ticket Issue B2B -------
            context['ticket_issue_b2b_date_filtered'] = TicketIssue.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(pnr__data_source__iexact="B2B")
            context['ticket_issue_b2b_date_filtered_count'] = TicketIssue.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).filter(pnr__data_source__iexact="B2B").count()
            # ------- Payment -------
            context['payment_date_filtered'] = Payment.objects.filter(created_at__range=(date_from_filtered, date_to_filtered))
            context['payment_date_filtered_count'] = Payment.objects.filter(created_at__range=(date_from_filtered, date_to_filtered)).count()
            context['payment_fields_count'] = len(Payment._meta.get_fields()) + 1
            context['payment_fields'] = dict([(f.name, f.verbose_name) for f in Payment._meta.fields + Payment._meta.many_to_many])
            context['can_view_payment'] = self.request.user.has_perm('payment.view_payment')
            # ------- Skytrip User -------
            context['skytrip_user_date_filtered'] = SkytripUser.objects.filter(date_joined__range=(date_from_filtered, date_to_filtered))
            context['skytrip_user_date_filtered_count'] = SkytripUser.objects.filter(date_joined__range=(date_from_filtered, date_to_filtered)).count()
            context['skytrip_user_fields_count'] = len(SkytripUser._meta.get_fields()) + 1
            context['skytrip_user_fields'] = dict([(f.name, f.verbose_name) for f in SkytripUser._meta.fields + SkytripUser._meta.many_to_many])
            context['can_view_skytrip_user'] = self.request.user.has_perm('user.view_skytripuser')
        return context


@method_decorator(login_required, name='dispatch')
class BlockedView(TemplateView):
    template_name = "exceptions/blocked.html"


@method_decorator(login_required, name='dispatch')
class AccessDeniedView(TemplateView):
    template_name = "exceptions/access-denied.html"
