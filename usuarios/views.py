# from rest_framework.views import APIView, Response, Request, status
# from django.shortcuts import get_object_or_404
# import ipdb

# from .models import Usuarios
# from .serializers import UsuariosSerializer


# class UsuariosView(APIView):
#     def get(self, request: Request) -> Response:
#         usuarios = Usuarios.objects.all().order_by("id")
#         serializer = UsuariosSerializer(usuarios, many=True)

#         return Response(serializer.data, status.HTTP_200_OK)

#     def post(self, request: Request) -> Response:
#         serializer = UsuariosSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         solicitacao = Usuarios.objects.create_user(**serializer.validated_data)

#         serializer = UsuariosSerializer(solicitacao)

#         return Response(serializer.data, status.HTTP_201_CREATED)


# class UsuariosDetailView(APIView):
#     def get(self, request: Request, id: int) -> Response:
#         usuario = get_object_or_404(Usuarios, id=id)
#         sereliazer = UsuariosSerializer(usuario)

#         return Response(sereliazer.data, status.HTTP_200_OK)
