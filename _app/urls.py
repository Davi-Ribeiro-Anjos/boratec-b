from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("clients.urls")),
    path("api/", include("branches.urls")),
    path("api/", include("employees.urls")),
    path("api/", include("employees_dismissals.urls")),
    path("api/", include("employees_epis.urls")),
    path("api/", include("pallets_controls.urls")),
    path("api/", include("pallets_movements.urls")),
    path("api/", include("pj_complements.urls")),
    path("api/", include("purchases_entries.urls")),
    path("api/", include("purchases_requests.urls")),
    path("api/", include("users.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
