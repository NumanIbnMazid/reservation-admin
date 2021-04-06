from django.urls import path, include
from .views import SkytripUserListView, SkytripUserDetailView, UserMediaListView, UserMediaDetailView

urlpatterns = [
    path("get-user-list/", SkytripUserListView.as_view(), name="user_list"),
    path("<id>/detail/", SkytripUserDetailView.as_view(), name="user_detail"),
    path("get-user-media-list/", UserMediaListView.as_view(), name="user_media_list"),
    path("media/<id>/detail/", UserMediaDetailView.as_view(), name="user_media_detail"),
]
