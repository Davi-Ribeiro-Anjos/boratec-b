from django.urls import path

from . import views

urlpatterns = [
    # path(
    #     "funcionarios/",
    #     views.FuncionariosView.as_view(),
    #     name="funcionarios",
    # ),
    path(
        "pj-complementos/<int:id>/",
        views.PJComplementosDetailView.as_view(),
        name="pj-complemento-id",
    ),
]
