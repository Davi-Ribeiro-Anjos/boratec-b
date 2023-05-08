from django.db import models


class Filiais(models.Model):
    id = models.IntegerField(primary_key=True)
    id_empresa = models.IntegerField()
    id_filial = models.IntegerField()
    id_garagem = models.IntegerField(unique=True)
    sigla = models.CharField(max_length=3, unique=True)
    nome = models.CharField(max_length=50, unique=True)
    uf = models.CharField(max_length=2)
    cnpj = models.CharField(max_length=14, unique=True)
