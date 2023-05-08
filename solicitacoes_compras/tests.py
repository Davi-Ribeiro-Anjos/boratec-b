from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse


from .models import SolicitacoesCompras
from usuarios.models import Usuarios
from filiais.models import Filiais
from .serializers import SolicitacoesComprasSerializer


class SolicitacoesComprasTestCase(APITestCase):
    url = reverse("solicitacoes-compras")
    solicitacao1 = {
        "numero_solicitacao": 45691124,
        "data_solicitacao_pra": "2023-05-01",
        "data_solicitacao_bo": "2023-05-01 09:15:32",
        "status": "ANDAMENTO",
        "filial": None,
        "solicitante": None,
    }
    solicitacao2 = {
        "numero_solicitacao": 45631242,
        "data_solicitacao_pra": "2023-05-02",
        "data_solicitacao_bo": "2023-05-05 09:30:32",
        "status": "ABERTO",
        "filial": None,
        "solicitante": None,
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
        Usuarios.objects.create_user(**self.usuario)
        Filiais.objects.create(**self.filial)

        self.solicitacao1["filial"] = 1
        self.solicitacao1["solicitante"] = 1

        res_post = self.client.post(self.url, self.solicitacao1)

        existe = SolicitacoesCompras.objects.filter(id=1).exists()

        self.assertTrue(existe)
        self.assertEqual(
            res_post.status_code, status.HTTP_201_CREATED, "status_code != 201"
        )

    def test_solic_compras_get_all(self):
        SolicitacoesCompras.objects.create(**self.solicitacao1)
        SolicitacoesCompras.objects.create(**self.solicitacao2)

        res = self.client.get(self.url)

        solicitacoes = SolicitacoesCompras.objects.all().order_by("-id")
        serializer = SolicitacoesComprasSerializer(solicitacoes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK, "status_code != 200")
        self.assertEqual(res.data, serializer.data, "os retornos são diferentes")
