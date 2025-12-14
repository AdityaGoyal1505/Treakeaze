from django.contrib import admin
from django.urls import path, include
from accounts.views import CombinedAuthView, custom_logout
from django.http import HttpResponse

def favicon_view(request):
    return HttpResponse(status=204)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", CombinedAuthView.as_view(), name="login"),
    path("logout/", custom_logout, name="logout"),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("conference/", include("conference.urls")),
    path("conference-mgmt/", include("conference_mgmt.urls")),

    path("favicon.ico", favicon_view),
]
