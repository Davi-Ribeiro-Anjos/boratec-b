from django.urls import path

from . import views

urlpatterns = [
    path(
        "epis/items/",
        views.EPIsItemsView.as_view(),
        name="epis-items",
    ),
]
