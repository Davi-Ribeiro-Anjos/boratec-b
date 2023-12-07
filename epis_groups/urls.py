from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.EPIsGroupsView.as_view(),
        name="epis-groups",
    ),
]
