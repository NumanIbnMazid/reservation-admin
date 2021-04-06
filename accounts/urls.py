from django.urls import path, include
from .views import (
    GroupCreateView, GroupUpdateView, delete_group, create_user, ProfileUpdateView, delete_user, NotExistsView, UserDetailView, GroupDetailView
)

urlpatterns = [
    path('', include('allauth.urls')),
    path("create-group/", GroupCreateView.as_view(), name="create_group"),
    path("group/<id>/update/", GroupUpdateView.as_view(), name="update_group"),
    path("delete-group/", delete_group, name="delete_group"),
    path("create-user/", create_user, name="create_user"),
    path("user/<slug>/update/", ProfileUpdateView.as_view(), name="update_user"),
    path("delete-user/", delete_user, name="delete_user"),
    path("user/<slug>/detail/", UserDetailView.as_view(), name="user_detail"),
    path("group/<id>/detail/", GroupDetailView.as_view(), name="group_detail"),
    # Block URLs
    path("signup/", NotExistsView.as_view(), name="not_exists")
]
