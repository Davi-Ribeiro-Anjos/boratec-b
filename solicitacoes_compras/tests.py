from datetime import datetime

from rest_framework.test import APITestCase
from rest_framework.views import status

from django.urls import reverse
from django.contrib.auth.models import User

from filiais.models import Filiais
from funcionarios.models import Funcionarios

from .models import SolicitacoesCompras
from .serializers import SolicitacoesComprasResponseSerializer


class SolicitacoesComprasTestCase(APITestCase):
    url = reverse("solicitacoes-compras")
    solicitacao1 = {
        "numero_solicitacao": 1,
        "data_solicitacao_bo": datetime.now(),
        "status": "ANDAMENTO",
        "solicitante": None,
        "filial": None,
        "autor": None,
        "ultima_atualizacao": None,
    }
    solicitacao2 = {
        "numero_solicitacao": 2,
        "data_solicitacao_bo": datetime.now(),
        "status": "ABERTO",
        "solicitante": None,
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
    funcionario = {
        "nome": "DAVI RIBEIRO",
        "empresa": "BORA",
        "tipo_contrato": "CLT",
        "cargo": "DESENVOLVEDOR",
        "data_admissao": "2023-04-04",
        "filial": None,
        "user": None,
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
        user = User.objects.create_user(**self.usuario)
        Funcionarios.objects.create(**self.funcionario, user=user)
        Filiais.objects.create(**self.filial)

        self.solicitacao1["filial"] = 1
        self.solicitacao1["autor"] = 1
        self.solicitacao1["solicitante"] = 1
        self.solicitacao1["ultima_atualizacao"] = 1

        res_post = self.client.post(self.url, self.solicitacao1)

        exists = SolicitacoesCompras.objects.filter(id=1).exists()

        self.assertTrue(exists)
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
        serializer = SolicitacoesComprasResponseSerializer(solicitacoes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK, "status_code != 200")
        self.assertEqual(res.data, serializer.data, "os retornos são diferentes")
        self.assertEqual(len(res.data), 2, "os tamanho é diferente")

    def test_solic_compras_get_by_id(self):
        User.objects.create_user(**self.usuario)
        Filiais.objects.create(**self.filial)

        self.solicitacao1["filial"] = 1
        self.solicitacao1["autor"] = 1
        self.solicitacao1["ultima_atualizacao"] = 1

        self.client.post(self.url, self.solicitacao1)

        res = self.client.get(self.url + "1/")

        solicitacoes = SolicitacoesCompras.objects.filter(id=1).first()
        serializer = SolicitacoesComprasResponseSerializer(solicitacoes)

        self.assertEqual(res.status_code, status.HTTP_200_OK, "status_code != 200")
        self.assertEqual(res.data, serializer.data, "os retornos são diferentes")
