from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def favicon_view(request):
    return HttpResponse(status=204)

urlpatterns = [
    path("admin/", admin.site.urls),

    # App URLs
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("conference/", include("conference.urls")),
    path("conference-mgmt/", include("conference_mgmt.urls")),

    # IMPORTANT: favicon handler
    path("favicon.ico", favicon_view),
]
