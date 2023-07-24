from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("clientes.urls")),
    path("api/", include("filiais.urls")),
    path("api/", include("funcionarios.urls")),
    path("api/", include("paletes_controles.urls")),
    path("api/", include("paletes_movimentos.urls")),
    path("api/", include("pj_complementos.urls")),
    path("api/", include("pj_contratos.urls")),
    path("api/", include("solicitacoes_compras.urls")),
    path("api/", include("solicitacoes_entradas.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
