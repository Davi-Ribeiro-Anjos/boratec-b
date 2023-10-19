from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from _service.get_media import GetMediaView, get_media

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("clients.urls")),
    path("api/", include("branches.urls")),
    path("api/", include("deliveries_histories.urls")),
    path("api/", include("employees.urls")),
    path("api/", include("employees_dismissals.urls")),
    path("api/", include("employees_epis.urls")),
    path("api/", include("epis_carts.urls")),
    path("api/", include("epis_groups.urls")),
    path("api/", include("epis_items.urls")),
    path("api/", include("epis_requests.urls")),
    path("api/", include("epis_sizes.urls")),
    path("api/", include("fleets_availabilities.urls")),
    path("api/", include("pallets_controls.urls")),
    path("api/", include("pallets_movements.urls")),
    path("api/", include("pj_complements.urls")),
    path("api/", include("purchases_entries.urls")),
    path("api/", include("purchases_requests.urls")),
    path("api/", include("users.urls")),
    path("api/", include("vehicles.urls")),
    path("api/", include("xmls.urls")),
    path(f"{settings.MEDIA_URL[1:-1]}/<path:path>", get_media, name="serve_media"),
    path(
        f"api/{settings.MEDIA_URL[1:-1]}/<path:path>/",
        GetMediaView.as_view(),
        name="get_media",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
