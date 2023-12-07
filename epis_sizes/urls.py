from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.EPIsSizesView.as_view(),
        name="epis-sizes",
    ),
    path(
        "<int:id>/",
        views.EPIsSizesDetailsView.as_view(),
        name="epis-sizes-id",
    ),
]
