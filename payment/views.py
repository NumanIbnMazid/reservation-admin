from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Payment, PaymentDetails
from util.helpers import (
    get_simple_object
)


class PaymentListView(ListView):
    template_name = "snippets/list-common.html"

    def get_queryset(self):
        qs = Payment.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(
            PaymentListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Payment List'
        context['page_short_title'] = 'Payment List'
        context['list_objects'] = self.get_queryset()
        context['fields_count'] = len(Payment._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in Payment._meta.fields + Payment._meta.many_to_many])
        context['namespace'] = 'payment'
        context["detail_url"] = "payment:payment_detail"
        context['can_add_change'] = True if self.request.user.has_perm(
            'payment.add_payment') == True and self.request.user.has_perm('payment.change_payment') == True else False
        context['can_view'] = self.request.user.has_perm(
            'payment.view_payment')
        context['can_delete'] = self.request.user.has_perm(
            'payment.delete_payment')
        return context


class PaymentDetailView(DetailView):
    template_name = "snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='id', model=Payment, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            PaymentDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Payment - {self.get_object().tran_id} Detail'
        context['page_short_title'] = f'Payment - {self.get_object().tran_id} Detail'
        context["list_url"] = "payment:payment_list"
        context['can_add_change'] = True if self.request.user.has_perm(
            'payment.add_payment') == True and self.request.user.has_perm('payment.change_payment') == True else False
        context['can_view'] = self.request.user.has_perm('payment.view_payment')
        context['can_delete'] = self.request.user.has_perm(
            'payment.delete_payment')
        return context


class PaymentDetailsListView(ListView):
    template_name = "payment/payment-details-list.html"

    def get_queryset(self):
        qs = PaymentDetails.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(
            PaymentDetailsListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'Payment Details List'
        context['page_short_title'] = 'Payment Details List'
        context['list_objects'] = self.get_queryset()
        context['fields_count'] = len(PaymentDetails._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in PaymentDetails._meta.fields + PaymentDetails._meta.many_to_many])
        context['namespace'] = 'payment-details'
        context["detail_url"] = "payment:payment_details_detail"
        context['can_add_change'] = True if self.request.user.has_perm(
            'payment.add_paymentdetails') == True and self.request.user.has_perm('payment.change_paymentdetails') == True else False
        context['can_view'] = self.request.user.has_perm(
            'payment.view_paymentdetails')
        context['can_delete'] = self.request.user.has_perm(
            'payment.delete_paymentdetails')
        return context


class PaymentDetailsDetailView(DetailView):
    template_name = "snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='id', model=PaymentDetails, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            PaymentDetailsDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'Payment - {self.get_object().payment.tran_id} Detail'
        context['page_short_title'] = f'Payment - {self.get_object().payment.tran_id} Detail'
        context["list_url"] = "payment:payment_list"
        context['can_add_change'] = True if self.request.user.has_perm(
            'payment.add_paymentdetails') == True and self.request.user.has_perm('payment.change_paymentdetails') == True else False
        context['can_view'] = self.request.user.has_perm('payment.view_paymentdetails')
        context['can_delete'] = self.request.user.has_perm(
            'payment.delete_paymentdetails')
        return context
