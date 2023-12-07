from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from _service.get_media import GetMediaView, get_media

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/authentications/", include("authentications.urls")),
    path("api/clients/", include("clients.urls")),
    path("api/branches/", include("branches.urls")),
    path("api/deliveries-histories/", include("deliveries_histories.urls")),
    path("api/employees/", include("employees.urls")),
    path("api/employees/dismissals/", include("employees_dismissals.urls")),
    path("api/employees/epis/", include("employees_epis.urls")),
    path("api/epis/carts/", include("epis_carts.urls")),
    path("api/epis/groups/", include("epis_groups.urls")),
    path("api/epis/items/", include("epis_items.urls")),
    path("api/epis/requests/", include("epis_requests.urls")),
    path("api/epis/sizes/", include("epis_sizes.urls")),
    path("api/fleets-availabilities/", include("fleets_availabilities.urls")),
    path("api/manuals/", include("manuals.urls")),
    path("api/pallets/controls/", include("pallets_controls.urls")),
    path("api/pallets/movements/", include("pallets_movements.urls")),
    path("api/pj/complements/", include("pj_complements.urls")),
    path("api/pj/thirteenths/", include("pj_thirteenths.urls")),
    path("api/purchases/entries/", include("purchases_entries.urls")),
    path("api/purchases/requests/", include("purchases_requests.urls")),
    path("api/roles/", include("roles.urls")),
    path("api/users/", include("users.urls")),
    path("api/vacancies/", include("vacancies.urls")),
    path("api/vehicles/", include("vehicles.urls")),
    path("api/xmls/", include("xmls.urls")),
    path(
        f"api/{settings.MEDIA_URL[1:-1]}/<path:path>/",
        GetMediaView.as_view(),
        name="get_media",
    ),
    path(f"{settings.MEDIA_URL[1:-1]}/<path:path>", get_media, name="serve_media"),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
