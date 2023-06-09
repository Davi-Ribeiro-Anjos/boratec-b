# from rest_framework.test import APITestCase
# from rest_framework.views import status
# from django.urls import reverse

# from .models import Usuarios
# from .serializers import UsuariosSerializer


# class SolicitacoesComprasTestCase(APITestCase):
#     url = reverse("usuarios")
#     # url_id = reverse("usuarios-id:id")
#     data1 = {
#         "username": "davi.bezerra",
#         "password": "bor@123",
#         "first_name": "davi",
#         "last_name": "bezerra",
#         "email": "davi.bezerra@bora.com.br",
#         "is_staff": False,
#         "is_superuser": False,
#     }
#     data2 = {
#         "username": "admin",
#         "password": "bor@123",
#         "first_name": "admin",
#         "last_name": "bora",
#         "email": "admin@bora.com.br",
#         "is_staff": True,
#         "is_superuser": True,
#     }

#     def test_usuarios_normal_post(self):
#         res_post = self.client.post(self.url, self.data1)

#         res_get = self.client.get(self.url).data
#         usuario = dict(*res_get)

#         self.assertEqual(
#             res_post.status_code, status.HTTP_201_CREATED, "status_code != 201"
#         )
#         self.assertFalse(
#             usuario["is_staff"] or usuario["is_superuser"],
#             "usuário não é normal",
#         )

#     def test_usuarios_super_user_post(self):
#         res_post = self.client.post(self.url, self.data2)

#         res_get = self.client.get(self.url).data
#         usuario = dict(*res_get)

#         self.assertEqual(
#             res_post.status_code, status.HTTP_201_CREATED, "status_code != 201"
#         )
#         self.assertTrue(
#             usuario["is_staff"] and usuario["is_superuser"],
#             "usuário não é super_usuario",
#         )

#     def test_usuarios_get_all(self):
#         Usuarios.objects.create(**self.data1)
#         Usuarios.objects.create(**self.data2)

#         res_get = self.client.get(self.url)

#         solicitacoes = Usuarios.objects.all().order_by("id")
#         serializer = UsuariosSerializer(solicitacoes, many=True)

#         self.assertEqual(res_get.status_code, status.HTTP_200_OK, "status_code != 200")
#         self.assertEqual(res_get.data, serializer.data, "os retornos são diferentes")
