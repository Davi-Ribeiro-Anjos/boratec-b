from django.urls import path

from . import views

urlpatterns = [
    path(
        "clients/",
        views.ClientsView.as_view(),
        name="clients",
    ),
    path(
        "clients/document/<int:id>/",
        views.DocumentView.as_view(),
        name="clients-document-id",
    ),
    path(
        "clients/choices/",
        views.ClientsChoicesView.as_view(),
        name="clients-choices",
    ),
]
