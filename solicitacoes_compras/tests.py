from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse

# from usuarios.models import Usuarios
from django.contrib.auth.models import User
from filiais.models import Filiais

from .models import SolicitacoesCompras
from .serializers import (
    SolicitacoesComprasSerializer,
    SolicitacoesComprasReponseSerializer,
)


class SolicitacoesComprasTestCase(APITestCase):
    url = reverse("solicitacoes-compras")
    solicitacao1 = {
        "numero_solicitacao": 45691124,
        "data_solicitacao_bo": "2023-05-01 09:15:32",
        "status": "ANDAMENTO",
        "filial": None,
        "autor": None,
        "ultima_atualizacao": None,
    }
    solicitacao2 = {
        "numero_solicitacao": 45631242,
        "data_solicitacao_bo": "2023-05-05 09:30:32",
        "status": "ABERTO",
        "filial": None,
        "autor": None,
        "solicitante": None,
        "ultima_atualizacao": None,
    }
    usuario = {
        "username": "davi.bezerra",
        "first_name": "davi",
        "last_name": "bezerra",
        "email": "davi.bezerra@bora.com.br",
        "is_staff": False,
        "is_superuser": False,
    }
    filial = {
        "id": 1,
        "id_empresa": 1,
        "id_filial": 1,
        "id_garagem": 1,
        "sigla": "SPO",
        "nome": "MAIRIPORA",
        "uf": "SP",
        "cnpj": "05504835000100",
    }

    def test_solic_compras_post(self):
        User.objects.create_user(**self.usuario)
        Filiais.objects.create(**self.filial)

        self.solicitacao1["filial"] = 1
        self.solicitacao1["autor"] = 1
        self.solicitacao1["ultima_atualizacao"] = 1

        res_post = self.client.post(self.url, self.solicitacao1)

        existe = SolicitacoesCompras.objects.filter(id=1).exists()

        self.assertTrue(existe)
        self.assertEqual(
            res_post.status_code, status.HTTP_201_CREATED, "status_code != 201"
        )

    def test_solic_compras_get_all(self):
        User.objects.create_user(**self.usuario)
        Filiais.objects.create(**self.filial)

        self.solicitacao1["filial"] = 1
        self.solicitacao1["autor"] = 1
        self.solicitacao1["ultima_atualizacao"] = 1

        self.solicitacao2["filial"] = 1
        self.solicitacao2["autor"] = 1
        self.solicitacao2["solicitante"] = 1
        self.solicitacao2["ultima_atualizacao"] = 1

        self.client.post(self.url, self.solicitacao1)
        self.client.post(self.url, self.solicitacao2)

        res = self.client.get(self.url)

        solicitacoes = SolicitacoesCompras.objects.all().order_by("id")
        serializer = SolicitacoesComprasReponseSerializer(solicitacoes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK, "status_code != 200")
        self.assertEqual(res.data, serializer.data, "os retornos são diferentes")
