from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("solicitacoes_compras.urls")),
    path("api/", include("solicitacoes_entradas.urls")),
    path("api/", include("usuarios_complementos.urls")),
    path("api/", include("paletes_controles.urls")),
    path("api/", include("paletes_movimentos.urls")),
    path("api/", include("filiais.urls")),
]
