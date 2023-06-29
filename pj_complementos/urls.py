from django.urls import path

from . import views

urlpatterns = [
    path(
        "pj-complementos/",
        views.PJComplementosView.as_view(),
        name="pj-complementos",
    ),
    path(
        "pj-complementos/<int:id>/",
        views.PJComplementosDetailView.as_view(),
        name="pj-complemento-id",
    ),
]
