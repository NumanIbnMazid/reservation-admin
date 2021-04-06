
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home, BlockedView, AccessDeniedView, HomeView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", home, name="home"),
    path("", HomeView.as_view(), name="home"),
    path('account/', include('accounts.urls')),
    path("user/", include(("user.urls", "user"), namespace="user")),
    path("pnr/", include(("pnr.urls", "pnr"), namespace="pnr")),
    path("ticket-issue/", include(("ticket_issue.urls", "ticket_issue"), namespace="ticket_issue")),
    path("payment/", include(("payment.urls", "payment"), namespace="payment")),
    path("util/", include(("util.urls", "util"), namespace="util")),
    path("setup/", include(("setup.urls", "setup"), namespace="setup")),
    # Exception URLS
    path('blocked/', BlockedView.as_view(), name='blocked'),
    path('access-denied/', AccessDeniedView.as_view(), name='access_denied'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
