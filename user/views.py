from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import SkytripUser, UserMedia
from util.helpers import (
    get_simple_object
)


class SkytripUserListView(ListView):
    template_name = "snippets/list-common.html"

    def get_queryset(self):
        qs = SkytripUser.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(
            SkytripUserListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'User List'
        context['page_short_title'] = 'User List'
        context['list_objects'] = self.get_queryset()
        context['fields_count'] = len(SkytripUser._meta.get_fields()) + 1
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in SkytripUser._meta.fields + SkytripUser._meta.many_to_many])
        context['namespace'] = 'user'
        context["detail_url"] = "user:user_detail"
        context['can_add_change'] = True if self.request.user.has_perm(
            'user.add_skytripuser') == True and self.request.user.has_perm('user.change_skytripuser') == True else False
        context['can_view'] = self.request.user.has_perm('user.view_skytripuser')
        context['can_delete'] = self.request.user.has_perm('user.delete_skytripuser')
        return context

    
class SkytripUserDetailView(DetailView):
    template_name = "snippets/detail-common.html"

    def get_object(self):
        return get_simple_object(key='id', model=SkytripUser, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            SkytripUserDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'User - {self.get_object().name} Detail'
        context['page_short_title'] = f'User - {self.get_object().name} Detail'
        context["list_url"] = "user:user_list"
        context['can_add_change'] = True if self.request.user.has_perm(
            'user.add_skytripuser') == True and self.request.user.has_perm('user.change_skytripuser') == True else False
        context['can_view'] = self.request.user.has_perm(
            'user.view_skytripuser')
        context['can_delete'] = self.request.user.has_perm(
            'user.delete_skytripuser')
        return context


class UserMediaListView(ListView):
    template_name = "media/media-list-datatable.html"

    def get_queryset(self):
        qs = UserMedia.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(
            UserMediaListView, self
        ).get_context_data(**kwargs)
        context['page_title'] = 'User Media List'
        context['page_short_title'] = 'User Media List'
        context['list_objects'] = self.get_queryset()
        context['fields_count'] = len(UserMedia._meta.get_fields()) + 2
        context['fields'] = dict([(f.name, f.verbose_name)
                                  for f in UserMedia._meta.fields + UserMedia._meta.many_to_many])
        context['namespace'] = 'user-media'
        context["detail_url"] = "user:user_media_detail"
        context['can_add_change'] = True if self.request.user.has_perm(
            'user.add_usermedia') == True and self.request.user.has_perm('user.change_usermedia') == True else False
        context['can_view'] = self.request.user.has_perm('user.view_usermedia')
        context['can_delete'] = self.request.user.has_perm(
            'user.delete_usermedia')
        return context

    
class UserMediaDetailView(DetailView):
    template_name = "user/detail-common.html"

    def get_object(self):
        return get_simple_object(key='id', model=UserMedia, self=self)

    def get_context_data(self, **kwargs):
        context = super(
            UserMediaDetailView, self
        ).get_context_data(**kwargs)
        context['page_title'] = f'User - {self.get_object().user.name} Media Detail'
        context['page_short_title'] = f'User - {self.get_object().user.name} Media Detail'
        context["list_url"] = "user:user_media_list"
        context['can_add_change'] = True if self.request.user.has_perm(
            'user.add_usermedia') == True and self.request.user.has_perm('user.change_usermedia') == True else False
        context['can_view'] = self.request.user.has_perm(
            'user.view_usermedia')
        context['can_delete'] = self.request.user.has_perm(
            'user.delete_usermedia')
        return context
