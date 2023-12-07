from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.EPIsItemsView.as_view(),
        name="epis-items",
    ),
]
