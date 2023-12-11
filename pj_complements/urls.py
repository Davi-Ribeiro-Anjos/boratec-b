from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.PJComplementsView.as_view(),
        name="pj-complements",
    ),
    path(
        "<int:id>/",
        views.PJComplementsDetailView.as_view(),
        name="pj-complements-id",
    ),
    path(
        "emails/",
        views.PJComplementsEmailView.as_view(),
        name="pj-complements-emails",
    ),
    path(
        "export/",
        views.PJComplementsExportView.as_view(),
        name="pj-complements-export",
    ),
]
