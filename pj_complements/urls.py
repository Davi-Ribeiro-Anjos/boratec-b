from django.urls import path

from . import views

urlpatterns = [
    path(
        "pj/complements/",
        views.PJComplementsView.as_view(),
        name="pj-complements",
    ),
    path(
        "pj/complements/<int:id>/",
        views.PJComplementsDetailView.as_view(),
        name="pj-complements-id",
    ),
]
