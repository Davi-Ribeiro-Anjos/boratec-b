from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.ClientsView.as_view(),
        name="clients",
    ),
    path(
        "document/<int:id>/",
        views.DocumentView.as_view(),
        name="clients-document-id",
    ),
    path(
        "choices/",
        views.ClientsChoicesView.as_view(),
        name="clients-choices",
    ),
]
