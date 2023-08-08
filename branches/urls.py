from django.urls import path

from . import views

urlpatterns = [
    path(
        "branches/",
        views.BranchesView.as_view(),
        name="branches",
    ),
]
