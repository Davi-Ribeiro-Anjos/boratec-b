from django.urls import path

from . import views

urlpatterns = [
    path(
        "epis/groups/",
        views.EPIsGroupsView.as_view(),
        name="epis-groups",
    ),
]
