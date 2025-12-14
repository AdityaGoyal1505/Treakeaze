from django.http import HttpResponse
from django.urls import path, include
from django.contrib import admin
from accounts.views import CombinedAuthView, custom_logout

def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nDisallow:",
        content_type="text/plain"
    )

def favicon_view(request):
    return HttpResponse(status=204)

urlpatterns = [
    path("admin/", admin.site.urls),

    # AUTH (keep it simple)
    path("login/", CombinedAuthView.as_view(), name="login"),
    path("logout/", custom_logout, name="logout"),

    # SYSTEM FILES (IMPORTANT)
    path("robots.txt", robots_txt),
    path("favicon.ico", favicon_view),

    # APPS
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("conference/", include("conference.urls")),
    path("conference-mgmt/", include("conference_mgmt.urls")),
]
