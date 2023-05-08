from rest_framework.test import APITestCase
from rest_framework.views import status
from django.urls import reverse


from .models import SolicitacoesCompras
from .serializers import SolicitacoesComprasSerializer


class SolicitacoesComprasTestCase(APITestCase):
    url = reverse("solicitacoes-compras")
    data1 = {
        "numero_solicitacao": 45691124,
        "data_solicitacao_pra": "2023-05-01",
        "data_solicitacao_bo": "2023-05-01 09:15:32",
        "status": "ANDAMENTO",
    }
    data2 = {
        "numero_solicitacao": 45631242,
        "data_solicitacao_pra": "2023-05-02",
        "data_solicitacao_bo": "2023-05-05 09:30:32",
        "status": "ABERTO",
    }

    def test_solic_compras_post(self):
        res_post = self.client.post(self.url, self.data1)

        existe = SolicitacoesCompras.objects.filter(id=1).exists()

        self.assertTrue(existe)
        self.assertEqual(
            res_post.status_code, status.HTTP_201_CREATED, "status_code != 201"
        )

    def test_solic_compras_get_all(self):
        SolicitacoesCompras.objects.create(**self.data1)
        SolicitacoesCompras.objects.create(**self.data2)

        res = self.client.get(self.url)

        solicitacoes = SolicitacoesCompras.objects.all().order_by("-id")
        serializer = SolicitacoesComprasSerializer(solicitacoes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK, "status_code != 200")
        self.assertEqual(res.data, serializer.data, "os retornos são diferentes")
