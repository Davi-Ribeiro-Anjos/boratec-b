from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("solicitacoes_compras.urls")),
    # path("api/", include("usuarios.urls")),
    path("api/", include("filiais.urls")),
]
